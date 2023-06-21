from django.test import TestCase
from django.test import Client, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.models import User, AnonymousUser
from profiles.models import Profile, ProductSet
from order.models import Order
from address.models import Address
from .models import Product
from django.urls import reverse
from profiles.views import accountInfo
from .views import showWishList

# Test for store.views.py
class StoreTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.product_1 = Product.objects.create(
            id = 1,
            title = "test product 1",
            description = "test product 1 is a fantastic phone",
            price = 540,
            brand = 'Apple',
            category = 'Smart Phone',
            rating = 4.5,
            stock = 4,
            discount = 12.50
        )
        self.product_2 = Product.objects.create(
            id = 2,
            title = "test product 2",
            description = "test product 2 is a fantastic laptop",
            price = 1080,
            brand = 'Samsung',
            category = 'Laptop',
            rating = 4.7,
            stock = 3,
            discount = 11.2
        )
        self.product_3 = Product.objects.create(
            id = 3,
            title = "test product 3",
            description = "test product 3 is a fantastic tablet",
            price = 820,
            brand = 'Lenovo',
            category = 'Tablet',
            rating = 4.7,
            stock = 3,
            discount = 11.2
        )

    def test_homepage(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertContains(response, '<p> Get the best deals on mobile phones and laptops from the comfort of home </p>')

    def test_get_products(self):
        response = self.client.get(reverse("products"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products.html")
        self.assertContains(response, "<strong>test product 1</strong>")
        self.assertContains(response, '<p class="price">Price £540</p>')

    def test_get_category(self):
        response = self.client.get(reverse('getCategory', args=['Smart Phone']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products.html")
        self.assertContains(response, "<strong>test product 1</strong>")
        self.assertContains(response, '<p class="price">Price £540</p>')
        self.assertNotContains(response, "<strong>test product 2</strong>")

    def test_get_brand(self):
        response = self.client.get(reverse('getBrand', args=['Samsung']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products.html")
        self.assertContains(response, "<strong>test product 2</strong>")
        self.assertContains(response, '<p class="price">Price £1080</p>')
        self.assertNotContains(response, "<strong>test product 1</strong>")

    def test_show_product_1(self):
        response = self.client.get(reverse('showProduct', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "showProduct.html")
        self.assertContains(response, "<h2>test product 1</h2>")
        self.assertContains(response, '<p>test product 1 is a fantastic phone</p>')
        self.assertNotContains(response, "test product 2 is a fantastic laptop")

    def test_show_product_2(self):
        response = self.client.get(reverse('showProduct', args=[2]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "showProduct.html")
        self.assertContains(response, "<h2>test product 2</h2>")
        self.assertContains(response, '<p>test product 2 is a fantastic laptop</p>')
        self.assertNotContains(response, "test product 1 is a fantastic phone")

    def test_show_wishlist_anon(self):
        request = self.factory.get('showWishList', {'wishlist': []})
        request.user = AnonymousUser()
        middleware = SessionMiddleware(request)
        middleware.process_request(request)
        request.session['wishlist'] = [1, 3]
        response = showWishList(request)
        self.assertTrue(response.status_code, 200)
        self.assertContains(response, '<h2>Wish List</h2>')
        self.assertContains(response, '<p>test product 1 is a fantastic phone</p>')
        self.assertContains(response, '<p>test product 3 is a fantastic tablet</p>')
        self.assertNotContains(response, '<p>test product 2 is a fantastic laptop</p>')
