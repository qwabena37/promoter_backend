from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    expertise = models.CharField(max_length=255, blank=True)