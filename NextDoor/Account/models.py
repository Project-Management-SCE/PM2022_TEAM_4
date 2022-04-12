from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
from django_google_maps import fields as map_fields


class CustomUser(AbstractUser):
    pass

class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='profile_image', default='profile_image/default_img.jpg')
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    bio = models.TextField(blank=True)
    address = map_fields.AddressField(max_length=200, blank=True)
    country = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    postal_code = models.CharField(max_length=255, blank=True)




    def __str__(self):
        return self.user.username





