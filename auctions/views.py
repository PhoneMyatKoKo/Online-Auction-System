from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.conf import settings
from .models import User,Listings,WatchList,Comments,BidRecord,WonAuctionRecord,Category
from django.contrib.auth.decorators import login_required
import datetime
import django.core.mail

def index(request):
    listing=Listings.objects.all()
  
    user=request.user
    category=Category.objects.all()
   

    context={"listings":listing, 'media_url':settings.MEDIA_URL,'user':user,"category":category,'hostname':request.META['HTTP_HOST']}    

    return render(request, "auctions/index.html",context)

#@login_required
def addListingsForm(request):
    if request.method=='GET':
        user=User.objects.all()
        category=Category.objects.all()
        context={'users':user,"category":category}
        return render(request,'auctions/registerListing.html',context)
    
    if request.method=='POST':
        name=request.POST['name']
        price=int(request.POST['price'])
        creatorId=int(request.POST['creator'])
        creator=User.objects.get(id=creatorId)
        image=request.FILES['img']
        description=request.POST['descript']
        categoryId=int(request.POST['category'])
        category=Category.objects.get(id=categoryId)

        listing=Listings(name=name,current_price=price,creator=creator,image=image,description=description,category=category.category_name)
        listing.save()
        return HttpResponse("Success")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()

        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


 #This is a utility function to find the maximun bid among bidders for the same listing.
 #Used in detailListing   
def findMax(Bidrecordlist):
   if not isinstance(Bidrecordlist[0],BidRecord):
      return "Error"
   max=Bidrecordlist[0].bidAmount
   maxObj=None
   for i in Bidrecordlist:
      if i.bidAmount>=max:
         max=i.bidAmount
         maxObj=i

   return maxObj     
      





def detailListing(request,pk):
     listing=Listings.objects.get(id=pk)
     comment=Comments.objects.filter(post=listing)
     if BidRecord.objects.filter(listing_id=pk).exists():
       bid_RecordList=BidRecord.objects.filter(listing_id=pk)
       bid_record=findMax(bid_RecordList)
    
     else:
       bid_record="0"

     if  WonAuctionRecord.objects.filter(listing_id=pk).exists():
        wr=WonAuctionRecord.objects.get(listing_id=pk)

     else:
        wr=None
    
         
       


     if request.user.is_authenticated:
         if WatchList.objects.filter(user_id=request.user.id).exists():
          wl=WatchList.objects.get(user_id=request.user.id)
     #Watch list listing
          listingList=wl.listing.all()
          duplicate=False

#Selected listings
     #global listing
     

     #Check duplicate
          for list in listingList:
         
           if(list.id==listing.id):
             duplicate=True
         else:    
          duplicate=False    
     else:
          duplicate=False         

     context={'listing':listing,'media_url':settings.MEDIA_URL,'Duplicate':duplicate,"comment":comment,"BidRecord":bid_record,"WinRecord":wr}
     return render(request,'auctions/Listingdetails.html',context)

@login_required
def watchList(request):
    user=request.user
    pk=user.id
    if(WatchList.objects.filter(user_id=pk).exists()):
     wl=WatchList.objects.get(user_id=pk)
     list=wl.listing.all()
     context={'listings':list,'media_url':settings.MEDIA_URL}

    else:
        context={'Message':"Your watch list is empty."} 
    return render(request,'auctions/watchList.html',context)


def addWatch(request,pk):
    if request.method=='POST':
     listing=Listings.objects.get(id=pk)
     wl=WatchList.objects.get(user_id=request.user.id)
     wl.listing.add(listing)
     return HttpResponseRedirect(reverse('watchList'))
    

def removeList(request,pk):
    if request.method=='POST':
      listing=Listings.objects.get(id=pk)
      wl=WatchList.objects.get(user_id=request.user.id)
      wl.listing.remove(listing)
      return HttpResponseRedirect(reverse('watchList'))
     
def watchlist_count(request):
   if request.user.is_authenticated:
    if WatchList.objects.filter(user_id=request.user.id).exists():
     wl=WatchList.objects.get(user_id=request.user.id)
     count=wl.listing.count()
    else:
       count=0  


   else:
      count=None 
   return {'count':count}

def category(request):
   category=Category.objects.all()
   return {"categoryListing":category}


# For Comment Adding-------------------------------------------------------
def add_comment(request,pk):
   userid=request.user.id
   postid=pk
   if request.method=='POST':
      comment_content=request.POST['comments']
      new_comment= Comments(content=comment_content,commentor_id=userid,post_id=postid)
      new_comment.save()
      return HttpResponseRedirect(reverse('detail',args=[postid]))
   
#For comment deleteing----------------------------------------
def delete_comment(request,pk):
 if  request.method=='POST':
   commentid=pk
   comment=Comments.objects.get(id=commentid)
   postid=comment.post_id
   comment.delete()
   return  HttpResponseRedirect(reverse('detail',args=[postid]))
 

def bidding(request,pk):
   bidder=request.user
   bidAmount=int (request.POST["bid"])
   listing=Listings.objects.get(id=pk)
   date=datetime.date.today()
   newBid=BidRecord(bidAmount=bidAmount,listing=listing,date=date,bidder=bidder)
   newBid.save()
   return HttpResponseRedirect(reverse('detail',args=[listing.pk]))

def closeAuction(request,pk):
   listing=Listings.objects.get(id=pk)
   listing.status=False
   listing.save()

   bid_recordlist=BidRecord.objects.filter(listing_id=pk)
   bid_record=findMax(bid_recordlist)

   wonAuction=WonAuctionRecord(finalAmount=bid_record.bidAmount,listing=bid_record.listing,winner=bid_record.bidder,date=datetime.date.today())
   wonAuction.save()
   if bid_record.bidder.email is not None:
       send_email(request,bid_record.bidder,bid_record.listing)
   return HttpResponseRedirect(reverse('detail',args=[listing.pk]))

def postedItems(request):
   pk=request.user.id
   listing=Listings.objects.filter(creator_id=pk)
   context={"listing":listing,'media_url':settings.MEDIA_URL}
   return render(request,'auctions/postedListing.html',context)

def wonItems(request):
   pk=request.user.id
   listing=[]
   if WonAuctionRecord.objects.filter(winner_id=pk).exists:
      wrList=WonAuctionRecord.objects.filter(winner_id=pk)
      for item in wrList:
         listing.append(item.listing)

   else:
      listing=None

   context={"listings":listing,'media_url':settings.MEDIA_URL}

   return render(request,'auctions/wonListings.html',context)         

def category_view(request,pk):
   category_id=pk
   category=Category.objects.get(id=pk)
   listing=Listings.objects.filter(category=category.category_name)
   context={"listings":listing,'category':category,"media_url":settings.MEDIA_URL}
   return render(request,'auctions/categorizedListings.html',context)

def search(request):
 #  send_email(request)
   key=request.GET['key']
   listings=Listings.objects.all()
   searchList=[]
   context={}
   for list in listings:
      listname=list.name.lower()
      if listname.__contains__(key):
         searchList.append(list)


   if searchList.__len__()!=0:
      context.__setitem__("searchList",searchList)
      context.__setitem__("media_url",settings.MEDIA_URL)
   else:
      context.__setitem__("searchList",None)

   return render(request,'auctions/searchListings.html',context)     


def send_email(request,winner,item):
   link='http://'+str(request.META['HTTP_HOST'])+'/listingDetail/'+str(item.pk)
   body=f'You have won the auction for {item}, Visit this link {link}'
   receiver=winner.email+""
   django.core.mail.send_mail("Congratulations "+winner.username,body,"phonemyatkoko_ph@cmu.ac.th",[receiver],False)
   
   
            
      