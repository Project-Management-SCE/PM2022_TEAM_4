from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model



class CustomUser(AbstractUser):
    pass

class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='profile_image', default='profile_image/def.jpg')
    latitude = models.FloatField(blank=True, null=True,default=31.253104)
    longitude = models.FloatField(blank=True, null=True,default=34.7892974)
    bio = models.TextField(blank=True)
    address = models.CharField(max_length=150, blank=True)
    country = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    postal_code = models.CharField(max_length=255, blank=True)




    def __str__(self):
        return self.user.username





