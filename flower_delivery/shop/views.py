from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from .models import Product, Order, CartItem
from .forms import OrderForm, CartItemForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .models import Product, Cart, CartItem
from .models import Cart, CartItem, Order, OrderItem

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


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Получаем или создаем корзину для текущего пользователя
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Получаем или создаем элемент корзины
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if created:
        cart_item.quantity = 1  # Устанавливаем количество по умолчанию
    else:
        cart_item.quantity += 1  # Увеличиваем количество, если элемент уже существует

    cart_item.save()

    return redirect('view_cart')  # Замените на ваше представление корзины

@login_required
def view_cart(request):
    try:
        # Найти корзину текущего пользователя
        cart = Cart.objects.get(user=request.user)
        # Получить все товары в корзине
        cart_items = CartItem.objects.filter(cart=cart)
    except Cart.DoesNotExist:
        # Если корзина не существует, создайте пустой список
        cart_items = []

    return render(request, 'shop/view_cart.html', {'cart_items': cart_items})


@login_required
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            # Получаем корзину текущего пользователя
            cart = Cart.objects.get(user=request.user)
            cart_items = CartItem.objects.filter(cart=cart)

            for item in cart_items:
                # Используйте цену продукта при создании OrderItem
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price  # Передаем цену
                )
                item.delete()  # Удаляем товар из корзины после добавления в заказ

            return redirect('order_success')  # Перенаправляем на страницу успеха
    else:
        form = OrderForm()
    return render(request, 'shop/create_order.html', {'form': form})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'shop/order_history.html', {'orders': orders})

@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

@login_required
def view_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'shop/view_orders.html', {'orders': orders})

@login_required
def order_success(request):
    return render(request, 'shop/order_success.html')
