import unittest
from django.contrib.auth import get_user_model

from .models import Product, Review

User = get_user_model()

class ProductModelTest(unittest.TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Test Product",
            price=100.00
        )

    def test_product_str(self):
        self.assertEqual(str(self.product), "Test Product")

    def test_average_rating(self):
        self.assertIsNone(self.product.average_rating)
        user = User.objects.create_user(username='testuser', password='testpassword')
        Review.objects.create(product=self.product, user=user, rating=5, comment="Great product")
        self.assertEqual(self.product.average_rating, 5.0)
