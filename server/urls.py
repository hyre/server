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

urlpatterns = [
    path('', user_views.home,name='home'),
    path('admin/', admin.site.urls),
    path('login/', user_views.auth_login, name='login'),
    path('logout/', user_views.auth_logout, name='logout'),
    path('signup/', user_views.signup, name='signup'),
    path('<username>/', user_views.user_profile, name='profile')
]
