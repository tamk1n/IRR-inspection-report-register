from collections.abc import Iterable
from typing import Any
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from base_user.models import MyUser
from manager.models import Company
from base_user.utils import UserPosition
from datetime import datetime, date
import pytz

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
        blank=True,
    )

    project = models.CharField(
        _('Project Name'),
        max_length=1000,
        null=True,
        blank=True
    )

    division = models.ForeignKey(
        'irr_app.Division',
        verbose_name=_('Division'),
        related_name='division_irs',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    field = models.CharField(
        _('Division field'),
        max_length=50,
        null=True,
        blank=True
    )

    responsible_person = models.CharField(
        _('Responsible Person'),
        max_length=50,
        null=True,
        blank=True
    )

    observations = models.ManyToManyField(
        'irr_app.Observation',
        related_name='ir',
        null=True,
        blank=True
    )

    ir_type = models.CharField(
        choices=[
            ('Negative', _('Negative')),
            ('Positive', _('Positive'))
        ],
        null=True,
        blank=True
    )
    image = models.ImageField(upload_to="evidences", null=True, blank=True)
    
    status = models.CharField(
        _('IR status'),
        choices=[
            ('Open', _('Open')),
             ('Close', _('Close')),
             ('Overdue', _('Overdue'))
        ],
        default='Open', null=True, blank=True)
    
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

        if not created: #and not self.close_date:
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
    
