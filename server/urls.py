"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import user.views as user_views
import company.views as company_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', user_views.home,name='home'),
    path('admin/', admin.site.urls),
    path('about-us/',user_views.about_us, name='about'),
    path('contact-us/',user_views.contact_us,name='contact'),
    path('manage/company/u/<username>', company_views.dashboard, name='dashboard'),
    path('manage/company/create/job',company_views.post_jobs,name='create-job'),
    path('manage/company/posted',company_views.posted_jobs,name='posted-jobs'),
    path('manage/company/application/<int:id>',company_views.view_applications,name='view-application'),
    path('login/', user_views.auth_login, name='login'),
    path('jobs/', user_views.JobListView.as_view(),name='job-list'),
    path('jobs/apply/<int:id>', user_views.job_apply, name='job-apply'),
    path('jobs/applications',user_views.applied_jobs,name='applications'),
    path('logout/', user_views.auth_logout, name='logout'),
    path('project/add',user_views.add_project,name='add-project'),
    path('signup/', user_views.signup, name='signup'),
    path('user/u/<username>/', user_views.user_profile, name='profile'),
    path('user/u/<username>/vouch/',user_views.vouchfn,name='vouch'),
    path('user/update', user_views.profile_update, name='update')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


handler404 = 'user.views.error404'