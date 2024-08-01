from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from .forms import OrderForm, CustomUserCreationForm, ReviewForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponseBadRequest, HttpResponse
from .models import Product, Cart, CartItem, Order, OrderItem, CustomUser
from .utils import is_within_working_hours  # Импортируйте функцию проверки рабочего времени
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

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

    if request.method == "POST":
        quantity = request.POST.get('quantity')
        if quantity:
            try:
                quantity = int(quantity)
                if quantity < 1:
                    return HttpResponseBadRequest("Количество должно быть больше нуля.")
            except ValueError:
                return HttpResponseBadRequest("Некорректное значение количества.")

            if created:
                cart_item.quantity = quantity  # Устанавливаем выбранное количество
            else:
                cart_item.quantity += quantity  # Увеличиваем количество на выбранное значение

        cart_item.save()
        return redirect('view_cart')  # Замените на ваше представление корзины

    # Для GET-запросов или если количество не указано, добавляем один товар
    if created:
        cart_item.quantity = 1  # Устанавливаем количество по умолчанию
    else:
        cart_item.quantity += 1  # Увеличиваем количество на 1

    cart_item.save()
    return redirect('view_cart')

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.get_total_price() for item in cart_items)

    return render(request, 'shop/view_cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })

@login_required
def remove_from_cart(request, cart_item_id):
    # Получаем элемент корзины по его ID
    cart_item = get_object_or_404(CartItem, id=cart_item_id)

    # Проверяем, что этот элемент принадлежит текущей корзине пользователя
    if cart_item.cart.user == request.user:
        cart_item.delete()

    return redirect('view_cart')


@login_required
def create_order(request):
    if not is_within_working_hours():
        return HttpResponse("Заказы принимаются только в рабочее время (09:00 - 18:00).")
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
def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

@login_required
def view_orders(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('orderitem_set__product')

    order_reports = []
    for order in orders:
        items = order.orderitem_set.all()
        total_price = sum(item.get_total_price() for item in items)

        order_data = {
            'order_id': order.id,
            'created_at': order.created_at,
            'items': items,
            'total_price': total_price,
            'status': order.status,
            'delivery_address': order.delivery_address,
            'payment_method': order.get_payment_method_display()
        }
        order_reports.append(order_data)

    context = {'order_reports': order_reports}
    return render(request, 'shop/view_orders.html', context)

@login_required
def order_success(request):
    return render(request, 'shop/order_success.html')

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            return redirect('product_detail', product_id=product.id)  # Redirect to product detail page
    else:
        form = ReviewForm()
    return render(request, 'shop/add_review.html', {'form': form, 'product': product})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.all()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product_detail', product_id=product_id)
    else:
        form = ReviewForm()

    return render(request, 'shop/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'form': form,
    })

#telegram
@csrf_exempt
def get_order_status(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        try:
            user = CustomUser.objects.get(username=username)
            orders = Order.objects.filter(user=user)
            order_statuses = []
            for order in orders:
                items = OrderItem.objects.filter(order=order)
                total_price = sum(item.get_total_price() for item in items)
                order_statuses.append({
                    'order_id': order.id,
                    'status': order.status,
                    'delivery_address': order.delivery_address,
                    'created_at': order.created_at.isoformat(),
                    'total_price': total_price,
                    'items': [
                        {'product_name': item.product.name, 'quantity': item.quantity}
                        for item in items
                    ],
                })
            return JsonResponse({'orders': order_statuses})
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)