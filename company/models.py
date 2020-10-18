from django.db import models
from user.models import Dev, Hr
# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=100)
    desc = models.TextField(max_length=200)

    def __repr__(self):
        return self.name
    
    def __str__(self):
        return self.name

class Job(models.Model):
    title = models.CharField(max_length=100)
    des = models.TextField(max_length=500)
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    posted_by = models.OneToOneField(Hr, on_delete=models.CASCADE)
    applicants = models.ManyToManyField(Dev,related_name="applied_jobs", blank=True)

    def __repr__(self):
        return self.company + ": " + self.title

    def __str__(self):
        return f"{self.title} opening in {self.company}"

class Application(models.Model):
    job_name = models.ForeignKey(Job, related_name="applications", on_delete=models.CASCADE)
    candidate = models.OneToOneField(Dev, related_name="application", on_delete=models.CASCADE)
    status = models.CharField(max_length=100) # Application Status

    def __str__(self):
        return f"Application for {self.job_name} by {self.candidate}"
