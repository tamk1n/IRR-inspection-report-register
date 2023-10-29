import os
from django.db import models
from django.utils.translation import gettext_lazy as _
from base_user.models import MyUser
from manager.models import Company
import uuid
from datetime import datetime, timedelta
import pytz
from engineer.tasks import set_token_inactive


# Create your models here.
class EngineerRegisterationToken(models.Model):
    token = models.UUIDField(
        _('Engineer Token'),
        default=uuid.uuid4,
        editable=False,
        null=True
    )
    expired_date = models.DateTimeField(blank=True, null=True, editable=False)
    is_expired = models.BooleanField(default=False)
    company = models.ForeignKey(
        Company,
        related_name='tokens',
        on_delete=models.CASCADE,
        null=True
    )

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        now = datetime.utcnow().replace(tzinfo=pytz.utc)
        # set token expiration date
        self.expired_date = self.expired_date or now + timedelta(
            days=int(os.getenv('ENGINEER_REGISTRATION_TOKEN_EXPIRE_IN_DAYS')))
        # check if token instance has been created
        # if instance already created (saving for INSERT or UPDATE) no need to create task
        create_task = True if self.pk is None else False
        super().save(force_insert, force_update, using, update_fields)

        # check if task to be created
        if create_task:
            # pass instance id as args (passing argument to be JSON serializable)
            # task will be executed after expired_date
            set_token_inactive.apply_async(args=[self.pk], eta=self.expired_date)

    def __str__(self) -> str:
        return "Token %s" % (self.token)