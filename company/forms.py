from django import forms
from company.models import Application

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['job_name','candidate','has_applied']

