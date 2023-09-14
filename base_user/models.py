from django.db import models
from django.contrib.auth.models import (AbstractBaseUser)
from django.conf import settings
# Create your models here.



USER_MODEL = settings.AUTH_USER_MODEL

class MyUser(AbstractBaseUser):
    username = models.CharField(
        _()
    )