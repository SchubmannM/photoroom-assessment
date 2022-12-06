import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    """A global abstract base model

    We have this because there are some fields/behaviors we want to consistently enforce everywhere.
    Every field in this should have a clear reason for existing and being required in all models.
    """

    created = models.DateTimeField(
        _("created"), editable=False, auto_now_add=True, null=True
    )
    updated = models.DateTimeField(
        _("updated"), editable=False, auto_now=True, null=True
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # append `updated` to update_fields if we save some of the fields in an object
        update_fields = kwargs.get("update_fields")
        if update_fields:
            kwargs.update(update_fields=list(update_fields) + ["updated"])
        super().save(*args, **kwargs)


class CustomUser(AbstractUser, BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return f'{self.email}'