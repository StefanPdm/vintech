# all variables in this file will be available to all views

import json
from . models import Order, OrderItem

def shopping_cart_items(request):
  if request.user.is_authenticated:
    current_user = request.user.customer
    current_order, created  = Order.objects.get_or_create(customer=current_user, completed=False)
      
    if current_order:
      cart_items_amount = current_order.get_total_quantity  
    else:
      cart_items_amount = 0
      
  else:
    cart_items_amount = 0
    try:
      shopping_card = json.loads(request.COOKIES['shopping_card'])
    except:
      shopping_card = {}
      
    for i in shopping_card:
      cart_items_amount += shopping_card[i]['quantity']
    
  return {"amount": cart_items_amount}