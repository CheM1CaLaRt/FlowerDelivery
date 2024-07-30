from django import forms
from .models import Order, CartItem
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['product', 'quantity']

class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['product', 'quantity']

class CustomUserCreationForm(UserCreationForm):
    phone = forms.CharField(required=False, max_length=15, help_text='Optional. Enter your phone number.')

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'password1', 'password2']
        help_texts = {
            'username': 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
            'email': 'Enter your email address.',
            'password1': 'Your password can’t be too similar to your other personal information. Your password must contain at least 8 characters. Your password can’t be a commonly used password. Your password can’t be entirely numeric.',
            'password2': 'Enter the same password as before, for verification.',
        }