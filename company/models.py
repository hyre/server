from django.db import models
from user.models import Dev, Hr
# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=100)
    desc = models.TextField(max_length=200)

class Job(models.Model):
    title = models.CharField(max_length=100)
    des = models.TextField(max_length=500)
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    posted_by = models.OneToOneField(Hr, on_delete=models.CASCADE)
    applicants = models.ManyToManyField(Dev,related_name="applied_jobs")