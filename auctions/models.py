from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import datetime


class User(AbstractUser):
    
    def __str__(self) :
        
        return self.username

class Category(models.Model):
    category_name=models.CharField(max_length=64)

    def __str__(self):
        return self.category_name+""   
    
class Listings(models.Model):
    name=models.CharField(max_length=16)
    current_price=models.IntegerField()
    description=models.TextField(blank=True)
    creator=models.ForeignKey(User,on_delete=models.CASCADE,)
    image=models.ImageField(null=True,blank=True,upload_to='images/')
    date=models.DateField(default=datetime.date.today())
    status=models.BooleanField(default=True)
    category=models.CharField(default="Uncategorized.",max_length=64)

    def __str__(self):
        return self.name
    
class WatchList(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,)
    listing=models.ManyToManyField(Listings,blank=True,null=True)   


    def __str__(self) :
        return self.user.username
    
class Comments(models.Model):
    content= models.TextField(blank=False)    
    commentor=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Listings,on_delete=models.CASCADE)

    def __str__(self) :
        return f'{self.commentor}\'s comment on {self.post}'
    


class BidRecord(models.Model):
    bidAmount=models.FloatField()
    listing=models.ForeignKey(Listings,on_delete=models.CASCADE)
    bidder=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateField(default=datetime.date.today())

    def __str__(self):
        return f'{self.bidder} made  a bid of {self.bidAmount} $ on {self.listing}.'
    
    def __lt__(self,anotherRecord):
        if(self.bidAmount<anotherRecord.bidAmount):
            return True
        return False
    
class WonAuctionRecord(models.Model):
    finalAmount=models.FloatField()
    listing=models.ForeignKey(Listings,on_delete=models.CASCADE)
    winner=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateField()

    def __str__(self):
        return f'{self.winner} won {self.listing}'    
    
 
    
