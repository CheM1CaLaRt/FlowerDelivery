# shop/admin.py

from django.contrib import admin
from .models import Product, Order, OrderItem

admin.site.register(Product)
# admin.site.register(Order)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'status', 'delivery_address', 'payment_method')
    list_filter = ('status', 'payment_method')
    search_fields = ('user__username', 'delivery_address')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    search_fields = ('order__id', 'product__name')