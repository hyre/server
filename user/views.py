from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, authenticate, logout
from user.forms import UserCreationForm, AuthForm,BioForm, SkillForm,ProjectForm
from user.models import Dev, Bio, Skill, Project, User, Vouch
from company.forms import ApplicationForm, HRBioForm
from company.models import Job, Application
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from company.views import dashboard


def home(request):
    return render(request,'index.html')

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
                return redirect('update')
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
        if request.method =='POST':
            hrbio  = HRBioForm(request.POST)
            if hrbio.is_valid:
                username = request.user.username
                hrbio.save()
                return redirect('dashboard',username=username)
        else:
            hrbio = HRBioForm(initial={'user': request.user})
        return render(request,'create_hr_profile.html',{'hrbio':hrbio})

@login_required
def add_project(request):
    if(request.method=='POST'):
        form = ProjectForm(request.POST)
        if form.is_valid:
            form.save()
            return user_profile(request,request.user.username)
    form = ProjectForm(initial={'user':request.user})
    return render(request,'add_project.html',{'form':form})




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
                    return redirect('profile',username=user.username)
                elif user.type == 'HR':
                    login(request,user)
                    return redirect('dashboard',username=user.username)
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
    auth_user = request.user
    user = Dev.objects.all().filter(username=username)
    if not user.exists():
        return redirect('home')

    user_base = User.objects.all().filter(username=username)[0]
    bio = user[0].bio
    skills = user[0].skill.skill_string.split(',')
    projects = Project.objects.all().filter(user=user[0])
    vouches = Vouch.objects.all().filter(user=user[0])
    vouched_hrs = [i.vouched_by for i in vouches]
    return render(request,'profile.html',{'user_base':user_base,'user':user,'bio':bio,'skills':skills,'projects':projects,'auth_user':auth_user,'vouches':vouches,'vouched_hrs':vouched_hrs})

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
    if(request.user.type=='DEV'):
        job = Job.objects.all().filter(id=id)
        if(request.method == 'POST'):
            application = Application()
            application.job_name = job[0]
            application.candidate = request.user
            application.has_applied = True
            application.save()
            return render(request,'application.html',{'message':'Application Success!'})
        else:
            application = Application.objects.all().filter(job_name=job[0])
            current_application = [i for i in application if i.candidate == request.user]
            try:
                if(current_application[0].has_applied):
                    return render(request,'application.html',{'message':'You have already applied to this post!'})
            except:
                application.job_name = job[0]
                application.candidate = request.user
                return render(request,'application.html',{'job':job[0]})
    else:
        return render(request,'404.html')
        

@login_required
def applied_jobs(request):
    if(request.user.type=='DEV'):
        applications = Application.objects.all()
        applied = []
        for i in applications:
            if i.candidate.username == request.user.username:
                applied.append(i)
        return render(request,'applied_jobs.html',{'applied':applied})
    else:
        return render(request,'404.html')

def error404(request,exception):
    return render(request,'404.html',status=404)

def about_us(request):
    return render(request,'about.html')

def contact_us(request):
    return render(request,'contact-us.html')

def vouchfn(request,username):
    vouch = Vouch()
    vouch.user = Dev.objects.all().filter(username=username)[0]
    vouch.vouched_by = request.user
    vouch.status = True
    vouch.save()
    return redirect('profile',username=username) 