from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    class Types(models.TextChoices):
        HR = "HR","Hr"
        DEV = "DEV", "Dev"

    base_type = Types.DEV

    type = models.CharField(
        _("Type"), max_length=50, choices=Types.choices, default=base_type
    )

    name = models.CharField(_("Name of the user"), blank=True, max_length=255)

    def save(self, *args, **kwargs):
        if not self.id:
            self.type = self.base_type
        return super().save(*args, **kwargs)


class HrManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.HR)

class DevManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.DEV)

class DevBio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500)

class Dev(User):
    base_type = User.Types.DEV
    objects = DevManager()

    @property
    def bio(self):
        return self.devbio

    class Meta:
        proxy = True

class Hr(User):
    base_type = User.Types.HR
    User.base_type = base_type
    objects = HrManager()

    class Meta:
        proxy = True

