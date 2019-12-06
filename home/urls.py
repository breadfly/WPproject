from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cart/', views.cart, name='cart'),
    path('books/', views.bookList, name='allBooks'),
    path('books/<category>/', views.bookList, name='books'),
    path('books/<category>/<isbn>/', views.detail, name='detail'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('mypage/', views.mypage, name="mypage"),
    path('thankyou/', views.purchase, name='purchase'),
    path('modify/', views.modifyAcc, name='modify'),
]