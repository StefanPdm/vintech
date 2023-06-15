import decimal
import json
from shop.models import *


def guestCookie(request):
  try:
    shopping_card = json.loads(request.COOKIES['shopping_card']) #read from cookie
  except:
    shopping_card = {} #create empty shopping card if no cookie
            
  articles = []
  order = {'get_total_price': 0, 'get_total_quantity': 0}
  amount = order['get_total_quantity']
  
  for i in shopping_card:
      amount += shopping_card[i]['quantity']
      article = Article.objects.get(id=i)
      sumary = article.price * decimal.Decimal(shopping_card[i]['quantity'])
      order['get_total_price'] += sumary
      order['get_total_quantity'] += shopping_card[i]['quantity']
      article = {'article':{'id':article.id, 'name':article.name, 'price':article.price, 'img': article.img},'quantity':shopping_card[i]['quantity'], 'get_sumary':sumary, }
      articles.append(article)
  print('return articles',articles)
  return {"articles": articles, "order": order}


def guestOrder(request, form_data):
  name = form_data['user_data']['name']
  email = form_data['user_data']['email']
  
  cookie_data = guestCookie(request)
  articles = cookie_data['articles']
  
  customer, created = Customer.objects.get_or_create(email=email) #get or create customer if email not exist
  customer.name = name
  customer.save()
  
  order = Order.objects.create(customer=customer, completed=False)
  for i in articles:
    article = Article.objects.get(id=i['article']['id'])
    order_item = OrderItem.objects.create(order=order, article=article, quantity=i['quantity'])
    
  return order, customer