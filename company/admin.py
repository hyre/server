from django.contrib import admin
from company.models  import Company, Job, Application
# Register your models here.
admin.site.register(Company)
admin.site.register(Job)
admin.site.register(Application)