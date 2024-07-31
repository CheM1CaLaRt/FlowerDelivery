from django import forms
from .models import Order, CartItem
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import OrderItem

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['delivery_address', 'payment_method']
        labels = {
            'delivery_address': 'Delivery Address',
            'payment_method': 'Payment Method'
        }
        widgets = {
            'payment_method': forms.RadioSelect
        }

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['payment_method'].initial = 'card'  # Устанавливаем значение по умолчанию

        # Убираем пустой вариант выбора
        self.fields['payment_method'].choices = [
            (key, value) for key, value in self.fields['payment_method'].choices if key
        ]

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['order', 'product', 'price', 'quantity']

class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']

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