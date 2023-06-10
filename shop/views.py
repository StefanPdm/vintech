from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import random


# Create your views here.


def shop(request):
    articles = Article.objects.all()
    random_article = random.choice(articles)
    old_price = random_article.price * 1.2
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
    else:
        articles = []
        order = []
        
    ctx = {"articles": articles, "random_article": random_article, "old_price":old_price, "order": order}
    return render(request, "shop.html", ctx)


def warenkorb(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        articles = order.orderitem_set.all()
        
    else:
        articles = []
        order = []
    ctx = {"articles": articles, "order": order}

    return render(request, "warenkorb.html", ctx)


def kasse(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        articles = order.orderitem_set.all()
    else:
        articles = []
        order = []
    ctx = {"articles": articles, "order": order}
    return render(request, "kasse.html", ctx)

def articleBackend(request):
    if request.method == 'POST':

        datas = json.loads(request.body)
  
        articleID = datas['articleID']
        action = datas['action']
        
        current_customer = request.user.customer
        current_article = Article.objects.get(id=articleID)
        
        order, created = Order.objects.get_or_create(customer=current_customer, completed=False)
        current_orderItem, created = OrderItem.objects.get_or_create(order=order, article=current_article)
     
        if action == 'addToShoppingCart':
            current_orderItem.quantity = (current_orderItem.quantity +1)
            
        elif action == 'removeFromShoppingCart':
            current_orderItem.quantity = (current_orderItem.quantity -1)
        
        current_orderItem.save()
        
        if current_orderItem.quantity <= 0:
            current_orderItem.delete()
            
    return JsonResponse("article_added", safe=False)