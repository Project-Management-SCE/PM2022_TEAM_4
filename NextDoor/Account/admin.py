import json
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile,CustomUser, RequestModel, MessageModel
from .form import CustomUserCreationForm, CustomUserChangeForm, RequestForm, MessageForm


CustomUser = get_user_model()

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email']


admin.site.register(CustomUser, CustomUserAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio', 'address']
    list_filter = ['user']

admin.site.register(UserProfile, ProfileAdmin)



class RequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'description', 'created_at', 'updated_at']
    list_filter = ['user']

admin.site.register(RequestModel, RequestAdmin)


class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'message', 'created_at', 'updated_at']
    list_filter = ['sender', 'receiver']

admin.site.register(MessageModel, MessageAdmin)
