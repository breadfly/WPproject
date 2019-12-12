from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name="logout"),
    path('mypage/', views.mypage, name="mypage"),
 
    path('market/', views.market, name='market'),
    path('market/<category>/', views.market, name='marketcategory'),
 
    path('auction/', views.auction, name='auction'),
    path('auction/<category>/', views.auction, name='auctioncategory'),
    path('detail/<pid>/', views.detail, name='detail'),

    path('sell/', views.sell, name='sell'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('myitems/', views.myitems, name='myitems'),
    path('myitems/sell/', views.sellitems, name='sellitems'),
    path('myitems/buy/', views.buyitems, name='buyitems'),


    # past
    path('cart/', views.cart, name='cart'),
    path('books/', views.bookList, name='allBooks'),
    path('books/<category>/', views.bookList, name='books'),
    path('books/<category>/<isbn>/', views.detail, name='detail'),
    path('thankyou/', views.purchase, name='purchase'),
    path('modify/', views.modifyAcc, name='modify'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

