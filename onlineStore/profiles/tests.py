from django.test import TestCase
from django.test import Client, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.models import User, AnonymousUser
from .models import Profile
from store.models import Product


class ProfileTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="testuser1")
        self.user1 = User.objects.get(username="testuser1")
        self.user1.set_password('password123')
        self.user1.save()
        self.client = Client()
        self.factory = RequestFactory()


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

        # User Login Failed
        login_2 = self.client.login(username='testuser1', password='I_Dont_Know')
        self.assertFalse(login_2)


    def test_addProductToWishlist(self):
        request = self.factory.post('/addFavourite', {'wishlist': []})
        middleware = SessionMiddleware(request)
        middleware.process_request(request)
        request.user = AnonymousUser()
        Profile.addProductToWishlist(request, '1')
        self.assertEqual(request.session['wishlist'], ['1'])

        #add to autheniticated user's wishlist