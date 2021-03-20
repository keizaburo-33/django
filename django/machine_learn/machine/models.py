from django.db import models


# Create your models here.

class User(models.Model):
    name: str = models.CharField(max_length=200)
    user_id: str = models.CharField(max_length=200)
    password: str = models.CharField(max_length=200)
