from collections.abc import Iterable
from typing import Any
from django.db import models
from django.utils.translation import gettext_lazy as _
from base_user.models import MyUser
from manager.models import Company
from base_user.utils import UserPosition
from datetime import datetime
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

    ir_type = models.CharField(
        choices=[
            ('Negative', _('Negative')),
            ('Positive', _('Positive'))
        ],
        null=True,
        blank=False
    )
    image = models.ImageField(upload_to="evidences", null=True)
    
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

    closed = models.BooleanField(
        _('IR closed'),
        default=False,
        null=True
    )

    def __str__(self) -> str:
        return "ÜYV %i" % (self.id)
    
    
    class Meta:
        ordering = ['-id']
    
    def save(self):
        now = datetime.utcnow().replace(tzinfo=pytz.utc)
        if (self.close_date and self.target_date < self.close_date) or (now > self.target_date):
            self.status = 'Overdue'
        elif self.closed:
            self.status = 'Close'
        else:
            self.status = 'Open'
        super().save()

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
    
