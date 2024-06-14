from django.contrib import admin
from .models import User,Listings,WatchList,Comments,BidRecord,WonAuctionRecord,Category

# Register your models here.
admin.site.register(User)
admin.site.register(Listings)
admin.site.register(WatchList)
admin.site.register(Comments)
admin.site.register(BidRecord)
admin.site.register(WonAuctionRecord)
admin.site.register(Category)