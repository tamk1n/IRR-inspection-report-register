from django.db import models
from django.utils.translation import gettext_lazy as _
from base_user.models import MyUser
from manager.models import Company


# Create your models here.
"""class Engineer(models.Model):
    engineer = models.OneToOneField(
        MyUser,
        on_delete=models.CASCADE,
        related_name='employee'
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='engineer'
    )"""