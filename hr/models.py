from django.db import models

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=100)
    desc = models.TextField(max_length=500)
    openings = models.IntegerField()
    