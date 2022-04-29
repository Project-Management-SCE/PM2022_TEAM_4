from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, resolve
from .form import CustomUserCreationForm, MessageForm, CommentForm, RequestForm# new
from .views import *
from .models import MessageModel,CommentModel,RequestModel
from .url import urlpatterns



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




# Create a class to test RequestModel model
class RequestModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='Bob', password='testBob123')
        self.request = RequestModel.objects.create(
            user=self.user,
            title='Test Request',
            description='Test Description',
        )

    def test_request_model(self):
        self.assertEqual(self.request.title, 'Test Request')
        self.assertEqual(self.request.description, 'Test Description')
        self.assertEqual(self.request.user, self.user)

    def test_request_model_str(self):
        self.assertEqual(str(self.request), 'Test Request')

    # Test RequesetForm
    def test_request_form(self):
        form = RequestForm(data={
            'title': 'Test Request',
            'description': 'Test Description',
        })
        self.assertTrue(form.is_valid())

    def test_request_form_invalid(self):
        form = RequestForm(data={
            'title': '',
            'description': 'Test Description',
        })
        self.assertFalse(form.is_valid())

    def test_request_form_invalid_title(self):
        form = RequestForm(data={
            'title': '',
            'description': 'Test Description',
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['title'], [u'This field is required.'])

    def test_request_form_invalid_description(self):
        form = RequestForm(data={
            'title': 'Test Request',
            'description': '',
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['description'], [u'This field is required.'])


# Create a class to test MessageModel model
class MessageModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='Bob', password='testBob123')
        # create another user
        self.user2 = get_user_model().objects.create_user(
            username='Bob2', password='testBob123')
        # create a message bob sends to bob2
        self.message = MessageModel.objects.create(
            sender=self.user,
            receiver=self.user2,
            message='Test Description',
        )

    def test_message_model(self):
        self.assertEqual(self.message.message, 'Test Description')
        self.assertEqual(self.message.sender, self.user)
        self.assertEqual(self.message.receiver, self.user2)

    def test_message_model_str(self):
        self.assertEqual(str(self.message), 'Test Description')

    # Test MessageForm
    def test_message_form(self):
        form = MessageForm(data={
            'message': 'Test Description',
        })
        self.assertTrue(form.is_valid())

    def test_message_form_invalid(self):
        form = MessageForm(data={
            'message': '',
        })
        self.assertFalse(form.is_valid())

    def test_message_form_invalid_message(self):
        form = MessageForm(data={
            'message': '',
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['message'], [u'This field is required.'])



# test CommentModel
class CommentModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='Bob', password='testBob123')
        # create a request for bob
        self.request = RequestModel.objects.create(
            title='Test Request',
            description='Test Description',
            user=self.user,
        )
        # create a comment for bob
        self.comment = CommentModel.objects.create(
            user=self.user,
            request=self.request,
            comment='Test Comment',
        )

    def test_comment_model(self):
        self.assertEqual(self.comment.comment, 'Test Comment')
        self.assertEqual(self.comment.user, self.user)
        self.assertEqual(self.comment.request, self.request)

    def test_comment_model_str(self):
        self.assertEqual(str(self.comment), 'Test Comment')

    # Test CommentForm
    def test_comment_form(self):
        form = CommentForm(data={
            'comment': 'Test Comment',
        })
        self.assertTrue(form.is_valid())

    def test_comment_form_invalid(self):
        form = CommentForm(data={
            'comment': '',
        })
        self.assertFalse(form.is_valid())

    def test_comment_form_invalid_comment(self):
        form = CommentForm(data={
            'comment': '',
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['comment'], [u'This field is required.'])


# UserProfile model test
class UserProfileTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='Bob', password='testBob123')
        # create userprofile for bob
        self.userprofile = UserProfile.objects.create(
            user=self.user,
            first_name='Bob',
            last_name='Bob',
            bio='Test Bio',
        )

    def test_userprofile_model(self):
        self.assertEqual(self.userprofile.user, self.user)
        self.assertEqual(self.userprofile.first_name, 'Bob')
        self.assertEqual(self.userprofile.last_name, 'Bob')
        self.assertEqual(self.userprofile.bio, 'Test Bio')

    def test_userprofile_model_str(self):
        self.assertEqual(str(self.userprofile), 'Bob')

    # Test UserProfileForm
    def test_userprofile_form(self):
        form = UserProfileForm(data={
            'first_name': 'Bob',
            'last_name': 'Bob',
            'bio': 'Test Bio',
        })
        self.assertTrue(form.is_valid())
























