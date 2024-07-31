# shop/urls.py

from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('create_order/', views.create_order, name='create_order'),
    path('view_orders/', views.view_orders, name='view_orders'),
    path('order_success/', views.order_success, name='order_success'),
    path('product_list/', views.product_list, name='product_list'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('accounts/', include('django.contrib.auth.urls')), # Встроенные URL-адреса для аутентификации
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('product/<int:product_id>/review/', views.add_review, name='add_review'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
]
