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
    path('order_backend/', views.orderBackend, name='order_backend'),
    path('active_order/<uuid:order_id>', views.activeOrder, name='active_order'), #alternative possible int:id, str:id, uuid:id, slug:id
    ]
