from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, resolve
# from models import CustomUser
from .form import CustomUserCreationForm # new
from .views import SignupPageView # new


class CustomUserTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='Bob',
            email='Bob@email.com',
            password='testBob123'
        )

        self.assertEqual(user.username, 'Bob')
        self.assertEqual(user.email, 'Bob@email.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username='Ashe',
            email='Ashe@email.com',
            password='testAshe123'
        )

        self.assertEqual(admin_user.username, 'Ashe')
        self.assertEqual(admin_user.email, 'Ashe@email.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

