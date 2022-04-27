from django.contrib.auth import get_user_model
from .models import UserProfile, RequestModel, MessageModel
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username')


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name','image', 'bio')


class RequestForm(ModelForm):
    class Meta:
        model = RequestModel
        fields = ('title', 'description' )


class MessageForm(ModelForm):
    class Meta:
        model = MessageModel
        fields = ('message',)