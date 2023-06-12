from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop, name='shop'),
    path('warenkorb/', views.warenkorb, name='warenkorb'),
    path('kasse/', views.kasse, name='kasse'),
    path('article_backend/', views.articleBackend, name='article_backend'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('register/', views.registerPage, name='register'),
    ]