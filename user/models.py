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

    # def save(self, *args, **kwargs):
    #     if not self.id:
    #         self.type = self.base_type
    #     return super().save(*args, **kwargs)


class HrManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.HR)

class DevManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.DEV)

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
    objects = HrManager()

    class Meta:
        proxy = True
    
    

class Bio(models.Model):
    user = models.OneToOneField(Dev, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500)

    def __str__(self):
        return f"{self.user}'s bio"

class Skill(models.Model):
    user = models.OneToOneField(Dev, on_delete=models.CASCADE)
    skill_string = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.user}"

class Project(models.Model):
    user = models.ForeignKey(Dev, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    link = models.URLField()
    desc = models.TextField(max_length=1000)

    def __str__(self):
        return f"{self.user} - {self.name}"


    
