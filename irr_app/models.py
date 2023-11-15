from collections.abc import Iterable
from typing import Any
from django.db import models
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from base_user.models import MyUser
from manager.models import Company
from base_user.utils import UserPosition
from irr_app.utils import (IRType, IRStatus)
from datetime import datetime, date
import pytz

class IRStatusQueryset(models.QuerySet):
    def negative(self):
        return self.filter(ir_type='Negative')

class IRStatusManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return IRStatusQueryset(self.model)
    
class InspectionReport(models.Model):
    date = models.DateField(blank=False)
    engineer = models.ManyToManyField(
        MyUser,
        verbose_name= _('Engineer'),
        help_text=_('Engineer'),
        limit_choices_to={
            'position': UserPosition.Engineer.value,
            'is_active': True
        },
        related_name='my_irs',
        null=True,
        blank=False,
    )

    project = models.CharField(
        _('Project Name'),
        max_length=1000,
        null=True,
        blank=False
    )

    division = models.ForeignKey(
        'irr_app.Division',
        verbose_name=_('Division'),
        related_name='division_irs',
        null=True,
        blank=False,
        on_delete=models.CASCADE
    )

    field = models.CharField(
        _('Division field'),
        max_length=50,
        null=True,
        blank=False
    )

    responsible_person = models.CharField(
        _('Responsible Person'),
        max_length=50,
        null=True,
        blank=False
    )

    observations = models.ManyToManyField(
        'irr_app.Observation',
        related_name='ir',
        null=True,
        blank=False
    )

    IR_TYPE_CHOICES = [(ir_type.name, ir_type.value) for ir_type in IRType]

    ir_type = models.CharField(
        choices=IR_TYPE_CHOICES,
        null=True,
        blank=False
    )

    image = models.ImageField(upload_to="evidences", null=True, blank=True)
    
    IR_STATUS_CHOICES = [(ir_status.name, ir_status.value) for ir_status in IRStatus]
    status = models.CharField(
        _('IR status'),
        choices=IR_STATUS_CHOICES,
        default=IR_STATUS_CHOICES[0],
        null=True,
        blank=True)
    
    target_date = models.DateField(
        _('IR target date'),
        null=True,
        blank=False,
    )

    close_date = models.DateField(
        _('Close date'),
        null=True,
        blank=True
    )
    objects = models.Manager()
    ir_status = IRStatusManager()

    def __str__(self) -> str:
        return "ÜYV %i" % (self.id)
      
    class Meta:
        ordering = ['-id']

    def clean(self):
        # Don't allow close date of ir in future.
        if self.close_date and self.close_date > date.today():
            raise ValidationError(_('You cannot define close date in future.'))
        
        # Don't allow close date before issue date.
        if self.close_date and self.close_date < self.date:
            raise ValidationError(_('Close date cannot be prior to issue date.'))
        
        return super().clean()
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        created = True if self.pk else False
        if self.close_date and self.status != 'Overdue':
            self.status = 'Close'

        super().save(force_insert, force_update, using, update_fields)

        if not created:
            from .tasks import set_ir_status
            set_ir_status.apply_async(args=[self.pk], eta=self.target_date)

    @property
    def observation_count(self):
        return self.observations.count()


class Division(models.Model):
    name = models.CharField(
        _("Division Name"),
        max_length=50,
        null=True,
        blank=True,
    )

    company = models.ForeignKey(
        Company,
        verbose_name=_("Division Company"),
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='company_dvs'
    )
    
    def __str__(self) -> str:
        return "%s" % (self.name)


class Observation(models.Model):
    content = models.TextField(null=True, blank=False)

    def __str__(self) -> str:
        return "Observation %s" % (self.id,)
    
