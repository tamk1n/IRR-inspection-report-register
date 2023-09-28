from django.db import models
from django.utils.translation import gettext_lazy as _
from base_user.models import MyUser
from base_user.utils import UserPosition

# Create your models here.

class InspectionReport(models.Model):
    date = models.DateTimeField()
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
        blank=True
    )

    project = models.CharField(
        _('Porject Name'),
        help_text='Project Name',
        max_length=1000,
        null=True, 
        blank=True
    )
    
    division = models.ManyToManyField(
        'irr_app.Divisions',
        verbose_name=_('Division'),
        related_name='division_irs',
        null=True,
        blank=True
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
        'irr_app.Observations',
        related_name='ir',
        null=True,
        blank=True
    )
    
    observation_type = models.CharField(
        choices=[
            ('NGT', _('Negative')),
            ('POS', _('Positive'))
        ],
        null=True,
        blank=True
    )

class Divisions(models.Model):
    name = models.CharField(
        _("Division Name"),
        max_length=50,
        null=True,
        blank=True
    )


class Observations(models.Model):
    content = models.TextField(null=True, blank=True)