# shop/urls.py

from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('create_order/', views.create_order, name='create_order'),
    path('order_history/', views.order_history, name='order_history'),
    path('product_list/', views.product_list, name='product_list'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('accounts/', include('django.contrib.auth.urls')),  # Встроенные URL-адреса для аутентификации
]
