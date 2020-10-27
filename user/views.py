from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, authenticate, logout
from user.forms import UserCreationForm, AuthForm #BioForm, SkillForm, ProjectForm
from user.models import Dev, Bio, Skill, Project, User
from company.models import Job, Application
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin



def home(request):
    return render(request,'base.html')

def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    elif request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def auth_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    elif request.method == 'POST':
        form = AuthForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password  = form.cleaned_data.get('password')
            user = authenticate(username=username,password=raw_password)
            print(user)
            if user is not None:
                if user.type == 'DEV':
                    login(request,user)
                    return render(request, 'devdash.html')
                elif user.type == 'HR':
                    login(request,user)
                    return render(request,'hrdash.html')
                else:
                    redirect('home')
            else:
                redirect('home')
    else:
        form = AuthForm()
        return render(request,'login.html',{'form':form})

def auth_logout(request):
    logout(request)
    return redirect('home')

def user_profile(request,username):
    user = Dev.objects.all().filter(username=username)
    if not user.exists():
        return redirect('home')

    user_base = User.objects.all().filter(username=username)[0]
    bio = user[0].bio.bio
    skills = user[0].skill.skill_string.split(',')
    projects = Project.objects.all().filter(user=user[0])
    return render(request,'profile.html',{'user_base':user_base,'user':user,'bio':bio,'skills':skills,'projects':projects})

# @login_required
# def user_profile_edit(request):

class JobListView(LoginRequiredMixin,ListView):
    ''' CUrrently all users can view posted jobs => limit this to dev users'''
    model = Job
    paginate_by = 10
    template_name = 'job_list.html'

@login_required
def job_apply(request,id):
    print(request.user)
    return redirect('home')