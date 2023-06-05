from django.shortcuts import render
from .models import *


# Create your views here.


def shop(request):
    articles = Article.objects.all()
    ctx = {"articles": articles}
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
