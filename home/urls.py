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
    path('sell/<pid>/', views.editProduct, name='editProduct'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('myitems/', views.myitems, name='myitems'),

    path('adminpage/', views.adminpage, name='adminpage'),
    path('userpage/<str:uid>', views.userpage, name='userpage'),
    path('categoryadd/', views.categoryadd, name='categoryadd'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

