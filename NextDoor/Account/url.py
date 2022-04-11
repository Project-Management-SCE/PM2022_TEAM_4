from django.contrib import admin
from django.urls import path
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import SignupPageView

urlpatterns = [
    path('signup/', SignupPageView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('user_profile/<str:pk_test>/', views.user_profile, name="user_profile"),
    path('user_profile/<str:pk_test>/edit/', views.edit_profile, name="edit_profile"),

]
