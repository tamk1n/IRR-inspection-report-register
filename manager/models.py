from django.db import models
from django.utils.translation import gettext_lazy as _
from base_user.models import MyUser
from base_user.utils import UserPosition
import uuid
import datetime

# Create your models here.

class Company(models.Model):
    name = models.CharField(
        _('Company name'),
        max_length=150,
        null=True,
        blank=True
    )
    about = models.TextField(
        _('Company Info'),
        null=True, 
        blank=True
    )
    managers = models.ManyToManyField(
        MyUser,
        verbose_name=_('QC Managers'),
        limit_choices_to={
            'position': UserPosition.Manager.value,
            'is_active': True
        },
        related_name='manager_company',
        blank=True,
    )
    employees = models.ManyToManyField(
        MyUser,
        limit_choices_to={
            'position': UserPosition.Engineer.value,
            'is_active': True
        },
        related_name='employee_company',
        blank=True,
    )
    
    class Meta():
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    def __str__(self) -> str:
        return (self.name).strip()
