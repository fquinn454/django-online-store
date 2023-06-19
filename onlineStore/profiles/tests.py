from django.test import TestCase
from django.test import Client, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.models import User, AnonymousUser
from .models import Profile, ProductSet
from store.models import Product

# TESTS FOR PROFILE
class ProfileTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="testuser1")
        self.user1 = User.objects.get(username="testuser1")
        self.user1.set_password('password123')
        self.user1.save()
        self.client = Client()
        self.factory = RequestFactory()
        self.product_1 = Product.objects.create(id=1, title='test_product1', description='A great phone ....', price=160, stock=3, rating=4.3, discount=3.5)
        self.product_3 = Product.objects.create(id=3, title='test_product3', description='A great tablet ....', price=360, stock=4, rating=4.25, discount=4.5)
        self.product_5 = Product.objects.create(id=5, title='test_product5', description='A great laptop ....', price=900, stock=4.5, rating=3.96, discount=6.5)
        self.productset_1 = ProductSet.objects.create(user = self.user1, product = self.product_1, quantity = 3)
        self.productset_3 = ProductSet.objects.create(user = self.user1, product = self.product_3, quantity = 2)
        self.productset_5 = ProductSet.objects.create(user = self.user1, product = self.product_5, quantity = 4)

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
        request = self.factory.post('addFavourite/<product_id>', {'wishlist': []})
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
        request = self.factory.post('addFavourite/<product_id>', {'wishlist': []})
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
        request = self.factory.get('/showWishList', {'wishlist': []})
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
        request = self.factory.get('/showWishList', {'wishlist': []})
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

    def test_removeProductFromWishlist(self):
        # Tests for anonymous user
        request = self.factory.post('removeWishListItem/<product_id>', {'wishlist': []})
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
        request = self.factory.post('removeWishListItem/<product_id>', {'wishlist': []})
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
        request = self.factory.post('deleteWishList', {'wishlist': []})
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
        request = self.factory.post('deleteWishList', {'wishlist': []})
        request.user = self.user1
        middleware = SessionMiddleware(request)
        middleware.process_request(request)
        self.assertTrue(request.user.is_authenticated)
        profile = Profile.objects.get(user = request.user)
        Profile.deleteWishList(request)
        self.assertEqual(set(profile.wishlist.all()), set([]))

    # TESTS FOR PRODUCTSETS
    def test_String_Productset(self):
        self.assertEqual(str(self.productset_1), 'test_product1 x 3' )
        self.assertEqual(str(self.productset_3), 'test_product3 x 2' )

    def test_getTotalCost(self):
        self.assertEqual(self.productset_1.getTotalCost(), 480 )
        self.assertEqual(self.productset_3.getTotalCost(), 720)

    def test_getCartItems(self):
        request = self.factory.get('showcart', {'cart': []})
        # For authenticated user
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

    def test_SumCart(self):
        request = self.factory.get('showcart', {'cart': []})
        # For authenticated user
        middleware = SessionMiddleware(request)
        middleware.process_request(request)
        request.user = AnonymousUser()
        request.session['cart'] = [3, 5]
        self.assertEqual(ProductSet.sumCart(request), 1260)
        request = self.factory.get('showcart', {'cart': []})
        # For authenticated user
        middleware = SessionMiddleware(request)
        middleware.process_request(request)
        request.user = self.user1
        profile = Profile.objects.get(user = request.user)
        profile.cart.add(self.productset_1)
        profile.cart.add(self.productset_5)
        self.assertEqual(ProductSet.sumCart(request), 4080)
