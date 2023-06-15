from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from .models import Profile


class ProfileTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="testuser1", password="password123", email="my_test_email@gmail.com")
        self.client = Client()

    def test_profile_string(self):
        """Profile returns string description"""
        user1 = User.objects.get(username="testuser1")
        profile = Profile.objects.get(user = user1)
        self.assertEqual(str(profile), 'testuser1')
        self.assertNotEqual(str(profile), 'testuser2')

    def test_user_loggedIn(self):
        user1 = User.objects.get(username="testuser1")
        login = self.client.login(username='testuser1', password='password123')
        login_2 = self.client.login(username='testuser2', password='I_Dont_Know')
        self.assertTrue(login)
        self.assertTrue(user1.is_authenticated)
        self.assertFalse(login_2)
