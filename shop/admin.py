from django.contrib import admin
from .models import *


class OrderAdmin(admin.ModelAdmin):
    
    list_display = ("customer", "order_date", "order_id", "completed", "get_total_price", "get_total_quantity")
    search_fields = ("customer", "order_date", "order_id", "completed")

# Register your models here.
admin.site.register(Customer)
admin.site.register(Article)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Address)
