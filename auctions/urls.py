from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('addListings',views.addListingsForm,name='addList'),
    path('listingDetail/<int:pk>',views.detailListing,name='detail'),
    path('watchList',views.watchList,name='watchList'),
    path('addWatchList/<int:pk>',views.addWatch,name='addWatch'),
    path('removeList/<int:pk>',views.removeList,name='removeList'),
    path('addComment/<int:pk>',views.add_comment,name='comment'),
    path('deleteCommetn/<int:pk>',views.delete_comment,name='delete_comment'),
    path('placeBid/<int:pk>',views.bidding,name='bidding'),
    path('closeAuction/<int:pk>',views.closeAuction,name="closeAuction"),
    path('postedItem',views.postedItems,name="postedItems"),
    path('wonItem',views.wonItems,name="wonItems"),
    path('category/<int:pk>',views.category_view,name='categoryView'),
    path('search/',views.search,name='search'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()