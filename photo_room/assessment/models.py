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
    teams = models.ManyToManyField('Team', through="TeamMembership")

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return f'{self.email}'


class ColorPalette(BaseModel):
    id = models.UUIDField(editable=False, default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=100, unique=True, null=True)
    colors = models.ManyToManyField('Color')
    created_by = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        colors = ''.join(str(color) for color in self.colors.all())
        return f'Name: {self.name} - Colors: {colors})'

class Color(BaseModel):
    id = models.UUIDField(editable=False, default=uuid.uuid4, primary_key=True)
    hex_code = models.CharField(max_length=7, default="#ffffff", unique=True)

    def __str__(self) -> str:
        return self.hex_code

class Team(BaseModel):
    id = models.UUIDField(editable=False, default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=100, unique=True, null=True)
    color_palettes = models.ManyToManyField('ColorPalette', through="TeamPalette")

class TeamMembership(BaseModel):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    team = models.ForeignKey('Team', on_delete=models.CASCADE)

class TeamPalette(BaseModel):
    palette = models.ForeignKey('ColorPalette', on_delete=models.CASCADE)
    team = models.ForeignKey('Team', on_delete=models.CASCADE)
