from django.contrib import admin
from django.urls import path
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import SignupPageView, create_request, requests, view_request
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #---------------------------- setUp user--------------------------------------#
    path('signup/', SignupPageView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('Rulse/', views.Rulse, name='Rulse'),
    #---------------------------- setUp user Profile--------------------------------------#
    path('user_profile/<str:pk_test>/', views.user_profile, name="user_profile"),
    path('user_profile/<str:pk_test>/edit/', views.edit_profile, name="edit_profile"),
    path('user_profile/<str:pk_test>/delete_user/', views.delete_user, name="delete_user"),
    path('user_profile/<str:pk_test>/create_request/', create_request, name="create_request"),
    path('user_profile/<str:pk_test>/requests/', requests, name="requests"),
    path('user_profile/<str:pk_test>/messaging/', views.messaging, name="messaging"),
    path('user_profile/<str:pk_test>/inbox/', views.inbox, name="inbox"),
    path('user_profile/<str:pk_test>/inbox/<int:pk>/messaging_read', views.messaging_read, name="messaging_read"),
    path('user_profile/<str:pk_test>/inbox/<int:pk>/messaging_delete', views.messaging_delete, name="messaging_delete"),
    path('user_profile/<str:pk_test>/view_request/<int:pk>/', view_request, name="view_request"),
    path('user_profile/<str:pk_test>/view_request/<int:pk>/delete_request/', views.delete_request, name="delete_request"),
    path('support_ticket/', views.support_ticket, name="support_ticket"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
