import decimal
from django.shortcuts import redirect, render
from .models import *
from django.http import JsonResponse, HttpResponse
import json
import random
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.forms import UserCreationForm # entfällt, da eigenes UserCreationForm erstellt
from . forms import UserRegisterForm
from shop.utils import *
import uuid
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from . views_tools import *
# ######## imports for PAYPAL ############################
from django.urls import reverse
from django.shortcuts import render
from paypal.standard.forms import PayPalPaymentsForm
# ######################################################


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
    old_price = random_article.price * decimal.Decimal(1.20)
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
        cookie_data = guestCookie(request)
        articles = cookie_data['articles']
        order = cookie_data['order']
        
    ctx = {"articles": articles, "order": order}
    return render(request, "warenkorb.html", ctx)


def kasse(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        articles = order.orderitem_set.all()
    else:
        cookie_data = guestCookie(request)
        articles = cookie_data['articles']
        order = cookie_data['order']
        
    ctx = {"articles": articles, "order": order}
    return render(request, "kasse.html", ctx)


def articleBackend(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        articleID = data['articleID']
        action = data['action']
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
            messages.info(request, 'Artikel wurde(n) aus dem Warenkorb entfernt')
        
        current_orderItem.save()
        
        if current_orderItem.quantity <= 0:
            current_orderItem.delete()
            
    return JsonResponse("article_added", safe=False)


def orderBackend(request):
    order_id = uuid.uuid4() # generate a unique id for the order, version 4
    if request.method == 'POST':
        form_data = json.loads(request.body)
        
        if request.user.is_authenticated:
            current_customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=current_customer, completed=False)
            
        else:
            order, current_customer = guestOrder(request, form_data)
    
        total_price = float(form_data['user_data']['total_price'])
        order.order_id = order_id
        order.completed = True
        order.save()

        Address.objects.create(
            customer=current_customer,
            order = order,
            address = form_data['invoice_data']['address'],
            plz = form_data['invoice_data']['plz'],
            city = form_data['invoice_data']['city'],
            bundesland = form_data['invoice_data']['bundesland'])
        
        # start for PAYPAL ####################################
        paypal_dict = {
        "business": "developer@heinemann.berlin",
        "amount": total_price,
        "item_name": "Bestellung bei VINTECH",
        "invoice": order_id,
        "currency_code": "EUR",
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('shop')),
        "cancel_return": request.build_absolute_uri(reverse('shop')),
        # "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }
        paypal_form = PayPalPaymentsForm(initial=paypal_dict)
        ctx = {"form_paypal": paypal_form} # if you want to render PP Btn on the page {{form_paypal}}
        # end for PAYPAL #################################### 
           
        order_URL = str(order_id)
        messages.success(request, mark_safe("Vielen Dank für Ihre <a href='/active_order/"+order_URL+"'>Bestellung: "+order_URL+"</a><br> Jetzt bezahlen: "+paypal_form.render()))
    
        # return JsonResponse("order_added", safe=False)
        response = HttpResponse('Bestellung wurde erfolgreich erstellt.')
        response.delete_cookie('shopping_card')
        return response



@login_required(login_url='/login/')
def activeOrder(request, order_id):
    order = Order.objects.filter(order_id=order_id)
    print('Order: ',order)
    if order and str(request.user) == str(Order.objects.get(order_id=order_id).customer):
        active_order = Order.objects.get(order_id=order_id)
        articles = active_order.orderitem_set.all()
        ctx = {"articles": articles, "active_order": active_order}
        return render(request, "active_order.html", ctx)
    else:
        return redirect('shop')


def handler404(request, exception=None, template_name='404.html'):
    return render(request, template_name, status=404)