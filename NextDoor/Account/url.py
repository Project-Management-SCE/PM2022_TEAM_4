from django.contrib import admin
from django.urls import path
from . import views
from django.urls import path
from . views import SignupPageView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', SignupPageView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]
