from django.test import TestCase
from django.test import Client, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.models import User, AnonymousUser
from .models import Profile, ProductSet
from order.models import Order
from address.models import Address
from store.models import Product
from django.urls import reverse
from .views import accountInfo

# Test for profiles.models.py
# Tests for Profile Class
class ProfileTestCase(TestCase):

    def setUp(self):
        User.objects.create(username="testuser1")
        self.user1 = User.objects.get(username="testuser1")
        self.user1.set_password('password123')
        self.user1.save()
        User.objects.create(username="testuser2")
        self.user2 = User.objects.get(username="testuser2")
        self.user2.set_password('password456')
        self.user2.save()
        self.client = Client()
        self.factory = RequestFactory()
        self.product_1 = Product.objects.create(id=1, title='test_product1', description='A great phone ....', price=160, stock=5, rating=4.3, discount=3.5)
        self.product_3 = Product.objects.create(id=3, title='test_product3', description='A great tablet ....', price=360, stock=4, rating=4.25, discount=4.5)
        self.product_5 = Product.objects.create(id=5, title='test_product5', description='A great laptop ....', price=900, stock=5, rating=3.96, discount=6.5)
        self.product_2 = Product.objects.create(id=2, title='test_product2', description='Another great phone ....', price=420, stock=5, rating=4.0, discount=3.8)
        self.productset_1 = ProductSet.objects.create(user = self.user1, product = self.product_1, quantity = 3)
        self.productset_3 = ProductSet.objects.create(user = self.user1, product = self.product_3, quantity = 2)
        self.productset_5 = ProductSet.objects.create(user = self.user1, product = self.product_5, quantity = 4)
        self.address = Address.objects.create(
            profile = Profile.objects.get(user=self.user1),
            line1 = "144 Long Lane",
            line2= "Aughton",
            city = "Ormskirk",
            postal_code = "L39 5DA"
        )

        self.order = Order.objects.create(
            profile = Profile.objects.get(user=self.user1),
            address = self.address,
        )

        productsets = [self.productset_1, self.productset_3]
        self.order.productsets.set(productsets)


    def test_profile_created_automatically(self):
        # check profile is automatically created when user is created
        self.assertTrue(Profile.objects.get(user=self.user1))
        profile = Profile.objects.get(user=self.user1)
        self.assertEqual(profile.user.username, 'testuser1')

    def test_profile_string(self):
        # Profile returns user.username as string
        user1 = User.objects.get(username="testuser1")
        profile = Profile.objects.get(user = user1)
        self.assertEqual(str(profile), 'testuser1')
        self.assertNotEqual(str(profile), 'testuser2')

    def test_user_loggedIn(self):
        # User Login Tests
        self.assertTrue(self.client.login(username='testuser1', password='password123'))
        self.assertTrue(self.user1.is_authenticated)
        self.client.logout()
        # User Login Failed
        login_2 = self.client.login(username='testuser1', password='I_Dont_Know')
        self.assertFalse(login_2)


    def test_addProductToWishlist(self):
        # Test addProducToWishlist()
        request = self.factory.post('addFavourite/<product_id>')
        request.user = AnonymousUser()
        middleware = SessionMiddleware(request)
        middleware.process_request(request)
        # Tests for Anonymous User
        self.assertFalse(request.user.is_authenticated)
        # Add product to empty wishlist
        Profile.addProductToWishlist(request, 1)
        self.assertEqual(set(request.session['wishlist']), set([1]))
        # Add product to wishlist with 1 item
        Profile.addProductToWishlist(request, 3)
        self.assertEqual(set(request.session['wishlist']), set([1, 3]))
        # Add product to wishlist with 2 items
        Profile.addProductToWishlist(request, 5)
        self.assertEqual(set(request.session['wishlist']), set([1, 3, 5]))
        # Add product already in wishlist
        Profile.addProductToWishlist(request, 5)
        self.assertEqual(set(request.session['wishlist']), set([1, 3, 5]))
        # Tests for Authenticated User
        request = self.factory.post('addFavourite/<product_id>')
        request.user = self.user1
        middleware = SessionMiddleware(request)
        middleware.process_request(request)
        self.assertTrue(request.user.is_authenticated)
        profile = Profile.objects.get(user = request.user)
        self.assertEqual(set(profile.wishlist.all()), set([]))
        # Add product to empty wishlist
        Profile.addProductToWishlist(request, 1)
        self.assertEqual(set(profile.wishlist.all()), set([self.product_1]))
        # Add product to wishlist with 1 item
        Profile.addProductToWishlist(request, 3)
        product_1 = Product.objects.get(id = 1)
        product_3 = Product.objects.get(id = 3)
        self.assertEqual(set(profile.wishlist.all()), set([product_1, product_3]))
        # Add product to wishlist with 2 items
        Profile.addProductToWishlist(request, 5)
        self.assertEqual(set(profile.wishlist.all()), set([product_1, product_3, self.product_5]))
        # Add product already in wishlist
        Profile.addProductToWishlist(request, 1)
        self.assertEqual(set(profile.wishlist.all()), set([product_1, product_3, self.product_5]))


    def test_getWishlistProducts(self):
        request = self.factory.get('/showWishList')
        request.user = AnonymousUser()
        middleware = SessionMiddleware(request)
        middleware.process_request(request)
        request.session['wishlist'] = [1, 3, 5]
        # Tests for Anonymous User
        self.assertFalse(request.user.is_authenticated)
        products = Profile.getWishlistProducts(request)
        self.assertEqual(set(products), set([self.product_1, self.product_3, self.product_5 ]))
        request.session['wishlist'] = []
        # Tests for Anonymous User
        self.assertFalse(request.user.is_authenticated)
        products = Profile.getWishlistProducts(request)
        self.assertEqual(set(products), set([]))

        # Tests for Authenticated user
        request = self.factory.get('showWishList')
        request.user = self.user1
        middleware = SessionMiddleware(request)
        middleware.process_request(request)
        self.assertTrue(request.user.is_authenticated)
        profile = Profile.objects.get(user = request.user)
        self.assertEqual(set(profile.wishlist.all()), set([]))
        products = Profile.getWishlistProducts(request)
        self.assertEqual(set(products), set([]))
        Profile.addProductToWishlist(request, 5 )
        products = Profile.getWishlistProducts(request)
        self.assertEqual(set(products), set([self.product_5]))
        Profile.deleteWishList(request)
        request = self.factory.get('showWishList', {'wishlist': []})
        middleware = SessionMiddleware(request)
        middleware.process_request(request)
        request.user = self.user1
        request.session['wishlist'] = [1, 3]
        self.assertTrue(request.user.is_authenticated)
        profile = Profile.objects.get(user = request.user)
        products = Profile.getWishlistProducts(request)
        self.assertEqual(set(products), set([self.product_1, self.product_3]))

    def test_removeProductFromWishlist(self):
        # Tests for anonymous user
        request = self.factory.post('removeWishListItem/<product_id>')
        request.user = AnonymousUser()
        middleware = SessionMiddleware(request)
        middleware.process_request(request)
        self.assertFalse(request.user.is_authenticated)
        Profile.addProductToWishlist(request, 1 )
        Profile.addProductToWishlist(request, 3 )
        Profile.addProductToWishlist(request, 5 )
        Profile.removeProductFromWishlist(request, 5 )
        self.assertEqual(set(Profile.getWishlistProducts(request)), set([self.product_1, self.product_3]))
        Profile.removeProductFromWishlist(request, 3 )
        self.assertEqual(set(Profile.getWishlistProducts(request)), set([self.product_1]))

        # tests for authenticated user
        request = self.factory.post('removeWishListItem/<product_id>')
        request.user = self.user1
        middleware = SessionMiddleware(request)
        middleware.process_request(request)
        self.assertTrue(request.user.is_authenticated)
        profile = Profile.objects.get(user = request.user)
        profile.wishlist.add(self.product_1)
        profile.wishlist.add(self.product_3)
        profile.wishlist.add(self.product_5)
        Profile.removeProductFromWishlist(request, 3)
        self.assertEqual(set(profile.wishlist.all()), set([self.product_1, self.product_5]))

    def test_deleteWishList(self):
        # test for anonymous user
        request = self.factory.post('deleteWishList')
        request.user = AnonymousUser()
        middleware = SessionMiddleware(request)
        middleware.process_request(request)
        self.assertFalse(request.user.is_authenticated)
        Profile.addProductToWishlist(request, 1 )
        Profile.addProductToWishlist(request, 3 )
        Profile.addProductToWishlist(request, 5 )
        Profile.deleteWishList(request)
        self.assertEqual(set(request.session['wishlist']), set([]))

        # test for authenticated user
        request = self.factory.post('deleteWishList')
        request.user = self.user1
        middleware = SessionMiddleware(request)
        middleware.process_request(request)
        self.assertTrue(request.user.is_authenticated)
        profile = Profile.objects.get(user = request.user)
        Profile.deleteWishList(request)
        self.assertEqual(set(profile.wishlist.all()), set([]))

    # Tests for ProductSet Class
    def test_String_Productset(self):
        self.assertEqual(str(self.productset_1), 'test_product1 x 3' )
        self.assertEqual(str(self.productset_3), 'test_product3 x 2' )

    def test_getTotalCost(self):
        self.assertEqual(self.productset_1.getTotalCost(), 480 )
        self.assertEqual(self.productset_3.getTotalCost(), 720)

    def test_getCartItems(self):
        request = self.factory.get('showcart')
        # Only authenticated users
        request.user = self.user1
        middleware = SessionMiddleware(request)
        middleware.process_request(request)
        # Add item to cart
        ProductSet.addProductToCart(request, 1)
        ProductSet.addProductToCart(request, 3)
        productsets = ProductSet.getCartItems(request)
        self.assertEqual(set(productsets), set([self.productset_1, self.productset_3]))
        # Remove item from cart
        ProductSet.removeProductFromCart(request, 1)
        productsets = ProductSet.getCartItems(request)
        self.assertEqual(set(productsets), set([self.productset_3]))

    def test_addProductToCart(self):
        request = self.factory.get('showcart')
        middleware = SessionMiddleware(request)
        middleware.process_request(request)
        request.user = self.user1
        ProductSet.addProductToCart(request, 2)
        profile = Profile.objects.get(user= request.user)
        productset_1 = ProductSet.objects.get(user = request.user, product=2)
        productset_2 = profile.cart.all()[0]
        self.assertEqual(productset_1, productset_2)
        request = self.factory.get('showcart')
        middleware = SessionMiddleware(request)
        middleware.process_request(request)
        request.user = AnonymousUser()
        # items already in cart
        request.session['cart'] = [1]
        ProductSet.addProductToCart(request, 3)
        self.assertEqual(set(request.session['cart']), set([1, 3]))
        request = self.factory.get('showcart')
        middleware = SessionMiddleware(request)
        middleware.process_request(request)
        request.user = AnonymousUser()
        request.session['cart'] = []
        ProductSet.addProductToCart(request, 1)
        self.assertEqual(set(request.session['cart']), set([1]))

    def test_removeItemFromCart(self):
        request = self.factory.get('showcart')
        middleware = SessionMiddleware(request)
        middleware.process_request(request)
        request.user = AnonymousUser()
        request.session['cart'] = [1, 3, 5, 7]
        ProductSet.removeProductFromCart(request, 5)
        self.assertEqual(set(request.session['cart']), set([1, 3, 7]))

    def test_SumCart(self):
        request = self.factory.get('showcart')
        # For authenticated user
        middleware = SessionMiddleware(request)
        middleware.process_request(request)
        request.user = AnonymousUser()
        request.session['cart'] = [3, 5]
        self.assertEqual(ProductSet.sumCart(request), 1260)
        request = self.factory.get('showcart')
        # For authenticated user
        middleware = SessionMiddleware(request)
        middleware.process_request(request)
        request.user = self.user1
        profile = Profile.objects.get(user = request.user)
        profile.cart.add(self.productset_1)
        profile.cart.add(self.productset_5)
        self.assertEqual(ProductSet.sumCart(request), 4080)
        middleware = SessionMiddleware(request)
        middleware.process_request(request)
        request.user = self.user1
        request.session['cart'] = [1, 5]
        profile = Profile.objects.get(user = request.user)
        # includes 1, 5 and £4080 from previous
        self.assertEqual(ProductSet.sumCart(request), 5140)

    def test_increment(self):
        request = self.factory.post('showcart')
        # Only authenticated users
        middleware = SessionMiddleware(request)
        middleware.process_request(request)
        request.user = self.user1
        profile = Profile.objects.get(user = request.user)
        profile.cart.add(self.productset_1)
        # Increment item in cart
        ProductSet.increment(request, 1)
        productsets = profile.cart.all()
        productset = productsets.get(product = self.product_1)
        self.assertEqual(productset.quantity, 4)
        self.assertFalse(productset.message)
        # Message True means we have reached stock limit - warning given
        ProductSet.increment(request, 1)
        productsets = profile.cart.all()
        productset = productsets.get(product = self.product_1)
        self.assertEqual(productset.quantity, 5)
        self.assertTrue(productset.message)
        ProductSet.increment(request, 1)
        productsets = profile.cart.all()
        productset = productsets.get(product = self.product_1)
        # Do not increment over stock limit
        self.assertEqual(productset.quantity, 5)
        self.assertTrue(productset.message)

    def test_decrement(self):
        request = self.factory.post('showcart')
        # Only authenticated users
        middleware = SessionMiddleware(request)
        middleware.process_request(request)
        request.user = self.user1
        profile = Profile.objects.get(user = request.user)
        profile.cart.add(self.productset_1)
        productsets = profile.cart.all()
        ProductSet.decrement(request, 1)
        productsets = profile.cart.all()
        productset = productsets.get(product = self.product_1)
        self.assertEqual(productset.quantity, 2)
        self.assertFalse(productset.message)
        ProductSet.decrement(request, 1)
        productsets = profile.cart.all()
        productset = productsets.get(product = self.product_1)
        self.assertEqual(productset.quantity, 1)
        self.assertFalse(productset.message)
        ProductSet.decrement(request, 1)
        # Doesn't decrement lower than 1
        productsets = profile.cart.all()
        productset = productsets.get(product = self.product_1)
        self.assertEqual(productset.quantity, 1)
        self.assertFalse(productset.message)

    # Tests for profiles.views.py
    def test_login_invalid_user(self):
        response=self.client.get(reverse('login'), follow = True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")

    def test_login_valid_user(self):
        response=self.client.post(reverse('login'), {'username': 'testuser1', 'password':'password123'}, follow = True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "showcart.html")


    def test_register_empty_data(self):
        user_data={

        }
        response=self.client.get(reverse('register'), user_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register.html")

    def test_register_invalid_data(self):
        user_data={
            'username': 'testuser3',
            'email':'testuser3@gmail.com',
            'password1':'password123',
            'password2':'password213'
        }
        response=self.client.post(reverse('register'), user_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register.html")

    def test_form_valid(self):
        user_data = {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'email': 'test@example.com',
        }
        response = self.client.post(reverse('register'), user_data)
        self.assertRedirects(response, '/showcart')
        self.assertEqual(response.status_code, 302)

    def test_get_Account_Info_LoggedIn(self):
        self.client.login(username="testuser1", password="password123")
        response = self.client.post(reverse('account-info'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account-info.html")
        self.assertContains(response, "144 Long Lane")

    def test_get_Account_Info_LoggedIn_asUser2(self):
        self.client.force_login(self.user2)
        response = self.client.post(reverse('account-info'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account-info.html")
        self.assertContains(response, '<p><strong>Username:</strong>testuser2</p>')


    def test_get_Account_Info_Not_Logged_In(self):
        response = self.client.post(reverse('account-info'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login')


    def test_noAddress_noOrders(self):
        request = self.factory.post('account-info')
        middleware = SessionMiddleware(request)
        middleware.process_request(request)
        request.user = self.user2
        response = accountInfo(request)
        self.assertEqual(response.status_code, 200)


