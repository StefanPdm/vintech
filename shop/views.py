from django.shortcuts import redirect, render
from .models import *
from django.http import JsonResponse
import json
import random
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.forms import UserCreationForm # entfällt, da eigenes UserCreationForm erstellt
from . forms import UserRegisterForm
from shop.utils import *


# Create your views here.

def registerPage(request):
    form = UserRegisterForm()
    ctx = {"form": form}
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False) # commit=False ->that we don't want to save the user
            user.save() # save the user
            customer = Customer(name=request.POST['username'], user=user)
            customer.save()
            order = Order(customer=customer)
            order.save()
            login(request, user)
            return redirect('shop')
        else:
            messages.error(request, 'Fehler bei Passworteingabe.')
    return render(request,'register.html', ctx)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('shop')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, "login.html")

def logoutPage(request):
    logout(request)
    return render(request,'logout.html')

def shop(request):
    articles = Article.objects.all()
    random_article = random.choice(articles)
    old_price = random_article.price * 1.2
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
    else:
        # articles = []
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
            # possible messages: debug, info, success, warning, error
            messages.info(request, 'Artikel wurde zum Warenkorb hinzugefügt')
             
        elif action == 'removeFromShoppingCart':
            current_orderItem.quantity = (current_orderItem.quantity -1)
            messages.info(request, '1 Artikel wurde aus dem Warenkorb entfernt')
        
        current_orderItem.save()
        
        if current_orderItem.quantity <= 0:
            current_orderItem.delete()
            
    return JsonResponse("article_added", safe=False)