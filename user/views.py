from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, authenticate, logout
from user.forms import UserCreationForm, AuthForm,BioForm, SkillForm
from user.models import Dev, Bio, Skill, Project, User
from company.forms import ApplicationForm
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
            login(request,user)
            if(user.type=='DEV'):
                return redirect('update')
            else:
                return hr_login(request)
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def profile_update(request):
    if(request.user.type=='DEV'):
        if request.method == 'POST':
            bio = BioForm(request.POST)
            skills = SkillForm(request.POST)
            if skills.is_valid and bio.is_valid:
                skills.save()
                bio.save()
                return user_profile(request,request.user.username)
        else:
            bio = BioForm(initial={'user': request.user})
            skills = SkillForm(initial={'user': request.user})
        return render(request, 'create_profile.html',{'bio':bio, 'skills':skills})
    else:
        return HttpResponse('404')

# Create a view to add projects


def hr_login(request):
    return render(request,'hrdash.html')

def auth_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    elif request.method == 'POST':
        form = AuthForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password  = form.cleaned_data.get('password')
            user = authenticate(username=username,password=raw_password)
            if user is not None:
                if user.type == 'DEV':
                    login(request,user)
                    return user_profile(request,user.username)
                elif user.type == 'HR':
                    login(request,user)
                    return hr_login(request)
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
    bio = user[0].bio
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
    ''' check if application exists if it does then already applied if not then show'''
    job = Job.objects.all().filter(id=id)
    if(application.has_applied):
        return HttpResponse("Already Applied!")
    else:
        if(request.method == 'POST'):
            application = Application()
            application.job_name = job[0]
            application.candidate = request.user
            application.has_applied = True
    return render(request,'application.html',{'job':job[0]})

@login_required
def applied_jobs(request):
    applications = Application.objects.all()
    array = []
    for i in applications:
        if i.candidate == request.user.username:
            array.append(i)
    return render(request,'applied_jobs.html',{'applications':array})