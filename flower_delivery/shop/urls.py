# shop/urls.py

from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('products/', views.product_list, name='product_list'),
    path('create_order/', views.create_order, name='create_order'),
    path('orders/', views.order_list, name='order_list'),
    path('accounts/', include('django.contrib.auth.urls')),  # Встроенные URL-адреса для аутентификации
]
