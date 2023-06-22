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
from .views import showWishList, removeWishListItem, delWishList, addToCart

# Test for store.views.py
class StoreTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        User.objects.create(username="testuser3")
        self.user3 = User.objects.get(username="testuser3")
        self.user3.set_password('password123')
        self.user3.save()
        self.profile_3 = Profile .objects.get(user = self.user3)
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
        self.productset_6 = ProductSet.objects.create(user = self.user3, product = self.product_1, quantity = 4)
        self.productset_7 = ProductSet.objects.create(user = self.user3, product = self.product_3, quantity = 1)


    def test_homepage(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertContains(response, '<p> Get the best deals on mobile phones and laptops from the comfort of home </p>')

    # Test product views
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

    # Test wishlist views
    def test_show_wishlist_anon(self):
        request = self.factory.get('showWishList')
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

    def test_show_wishlist_user(self):
        self.client.force_login(self.user3)
        productsets = [1, 3]
        self.profile_3.wishlist.set(productsets)
        response = self.client.get(reverse('showWishList'))
        self.assertTrue(response.status_code, 200)
        self.assertContains(response, '<h2>Wish List</h2>')
        self.assertContains(response, '<p>test product 1 is a fantastic phone</p>')
        self.assertContains(response, '<p>test product 3 is a fantastic tablet</p>')
        self.assertNotContains(response, '<p>test product 2 is a fantastic laptop</p>')

    def test_add_favourite_anon(self):
        response = self.client.get(reverse('addFavourite', args=[3]))
        self.assertTrue(response.status_code, 302)
        response = self.client.get(reverse('addFavourite', args=[2]), follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertContains(response, '<span class="badge">2</span></a>')

    def test_add_favourite_user(self):
        self.client.force_login(self.user3)
        productsets = [1]
        self.profile_3.wishlist.set(productsets)
        response = self.client.get(reverse('addFavourite', args=[3]), follow = True)
        self.assertTrue(response.status_code, 200)
        self.assertContains(response, '<span class="badge">2</span></a>')
        self.assertEqual(set(self.profile_3.wishlist.all()), set([self.product_1, self.product_3]))

    def test_remove_product_anon(self):
        request = self.factory.get('removeWishListItem')
        request.user = AnonymousUser()
        middleware = SessionMiddleware(request)
        middleware.process_request(request)
        request.session['wishlist'] = [1, 3]
        response = removeWishListItem(request, 3)
        self.assertTrue(response.status_code, 302)
        self.assertTrue(request.session['wishlist'], [self.productset_6])

    def test_remove_product_user(self):
        self.client.force_login(self.user3)
        productsets = [1, 2, 3]
        self.profile_3.wishlist.set(productsets)
        response = self.client.get(reverse('removeWishListItem', args=[1]), follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertContains(response, '<span class="badge">2</span></a>')
        self.assertEqual(set(self.profile_3.wishlist.all()), set([self.product_2, self.product_3]))

    def test_delete_wishlist_anon(self):
        request = self.factory.get('deleteWishList')
        request.user = AnonymousUser()
        middleware = SessionMiddleware(request)
        middleware.process_request(request)
        request.session['wishlist'] = [1, 3]
        response = delWishList(request)
        self.assertTrue(response.status_code, 302)
        self.assertEqual(request.session['wishlist'], [])

    def test_delete_wishlist_user(self):
        self.client.force_login(self.user3)
        productsets = [1, 2]
        self.profile_3.wishlist.set(productsets)
        response = self.client.get(reverse('deleteWishList'), follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertContains(response, '<span class="badge">0</span></a>')
        self.assertEqual(set(self.profile_3.wishlist.all()), set([]))

    def test_show_cart_anon(self):
        response = self.client.get(reverse('showcart'), follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertContains(response, '<h2>Log In</h2>')
        self.assertTemplateUsed(response, "registration/login.html")

    def test_show_cart_user(self):
        self.client.force_login(self.user3)
        productsets = [self.productset_6, self.productset_7]
        self.profile_3.cart.set(productsets)
        response = self.client.get(reverse('showcart'), follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertContains(response, '<h2>Cart</h2>')
        self.assertTemplateUsed(response, "showcart.html")
        self.assertContains(response, '<p>test product 1</p>')
        self.assertContains(response, '<p>test product 3</p>')
        self.assertNotContains(response, '<p>test product 2</p>')

    def test_add_to_cart_anon(self):
        request = self.factory.post('addToCart')
        request.user = AnonymousUser()
        middleware = SessionMiddleware(request)
        middleware.process_request(request)
        request.session['cart'] = [1, 3]
        response = addToCart(request, 2)
        self.assertTrue(response.status_code, 302)
        self.assertEqual(set(request.session['cart']), set([1, 2, 3]))

    def test_add_to_cart_user(self):
        self.client.force_login(self.user3)
        productsets = [self.productset_7]
        self.profile_3.cart.set(productsets)
        response = self.client.post(reverse('addToCart', args=[1]), follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertContains(response, '<span class="badge">2</span></a>')
        self.assertEqual(set(self.profile_3.cart.all()), set([self.productset_6, self.productset_7]))


