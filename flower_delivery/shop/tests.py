import unittest

from django.contrib.auth import get_user_model
from .models import Product, Cart, CartItem, Review

class ProductModelTest(unittest.TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Test Product",
            price=100.00
        )

    def test_product_string_representation(self):
        self.assertEqual(str(self.product), "Test Product")

    def test_average_rating(self):
        user = get_user_model().objects.create_user(username="testuser", password="12345")
        Review.objects.create(product=self.product, user=user, rating=5, comment="Great!")
        Review.objects.create(product=self.product, user=user, rating=3, comment="Okay.")
        self.assertEqual(self.product.average_rating, 4.0)

class CartItemModelTest(unittest.TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser", password="12345")
        self.product = Product.objects.create(
            name="Test Product",
            price=100.00
        )
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)

    def test_cart_item_string_representation(self):
        self.assertEqual(str(self.cart_item), "Test Product (2)")

    def test_get_total_price(self):
        self.assertEqual(self.cart_item.get_total_price(), 200.00)

if __name__ == '__main__':
   unittest.main()