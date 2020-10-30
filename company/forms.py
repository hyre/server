from django import forms
from company.models import Application, HR_bio, Job

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['job_name','candidate','has_applied']

class HRBioForm(forms.ModelForm):
    class Meta:
        model = HR_bio
        fields = ['user','works_for','location']

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title','des','company','posted_by']
