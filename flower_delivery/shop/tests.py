from django.test import TestCase
from django.contrib.auth.models import User
from .models import Product, Order

class ShopTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.product = Product.objects.create(name='Test Product', price=10.00)

    def test_create_order(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post('/create_order/', {'products': [self.product.id]})
        self.assertEqual(response.status_code, 302)
        order = Order.objects.first()
        self.assertEqual(order.user, self.user)
        self.assertIn(self.product, order.products.all())