from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, resolve
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


class SignupTests(TestCase):  # new
    username = 'BobTheTester'
    email = 'newuser@email.com'

    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)

    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'Account/signup.html')
        self.assertContains(self.response, 'Sign Up')
        self.assertNotContains(
            self.response, 'invalid Page.')

    def test_signup_form(self):  # new
        form = self.response.context.get('form')

        self.assertIsInstance(form, CustomUserCreationForm)
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_signup_view(self): # new
        view = resolve('/Account/signup/')
        self.assertEqual(
        view.func.__name__,
        SignupPageView.as_view().__name__)

