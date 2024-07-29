from django import forms
from .models import Order, CartItem

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['product', 'quantity']

class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['product', 'quantity']
