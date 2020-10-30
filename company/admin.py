from django.contrib import admin
from company.models  import Company, Job, Application, HR_bio
# Register your models here.
admin.site.register(Company)
admin.site.register(Job)
admin.site.register(Application)
admin.site.register(HR_bio)