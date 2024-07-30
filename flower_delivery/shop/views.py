from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from .models import Product, Order, CartItem
from .forms import OrderForm, CartItemForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()
def index(request):
    products = Product.objects.all()
    return render(request, 'shop/index.html', {'products': products})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if request.method == 'POST':
        form = CartItemForm(request.POST, instance=cart_item)
        if form.is_valid():
            form.save()
            return redirect('view_cart')
    else:
        form = CartItemForm(instance=cart_item)
    return render(request, 'shop/add_to_cart.html', {'form': form, 'product': product})

@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.get_total_price() for item in cart_items)
    return render(request, 'shop/view_cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def create_order(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if request.method == 'POST':
        for item in cart_items:
            Order.objects.create(
                user=request.user,
                product=item.product,
                quantity=item.quantity,
                total_price=item.get_total_price(),
                status='Pending'
            )
        cart_items.delete()
        return redirect('order_history')
    return render(request, 'shop/create_order.html', {'cart_items': cart_items})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'shop/order_history.html', {'orders': orders})

@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})
