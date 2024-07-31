# shop/admin.py

from django.contrib import admin
from .models import Product, Order, OrderItem
from .models import Review


# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user', 'created_at', 'status', 'delivery_address', 'payment_method')
#     list_filter = ('status', 'payment_method', 'created_at')
#     search_fields = ('user__username', 'delivery_address')
#     fields = ('user', 'delivery_address', 'payment_method', 'status', 'created_at')
#     readonly_fields = ('user', 'delivery_address', 'payment_method', 'created_at')
#
#     def get_readonly_fields(self, request, obj=None):
#         if obj:  # при редактировании существующего объекта
#             return self.readonly_fields + ('user', 'delivery_address', 'payment_method', 'created_at')
#         return self.readonly_fields

admin.site.register(Order)
admin.site.register(Product)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'created_at','comment')
    list_filter = ('product', 'rating')
    search_fields = ('user__username', 'product__name', 'comment')


