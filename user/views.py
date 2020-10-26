from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, authenticate, logout
from user.forms import UserCreationForm #BioForm, SkillForm, ProjectForm
from django.contrib.auth.forms import AuthenticationForm
from user.models import Dev, Bio, Skill, Project
from django.contrib.auth.decorators import login_required


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
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def auth_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    elif request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
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
        form = AuthenticationForm()
        return render(request,'login.html',{'form':form})

def auth_logout(request):
    logout(request)
    return redirect('home')

def user_profile(request,username):
    user = Dev.objects.all().filter(username=username)
    if not user.exists():
        return redirect('home')
    return render(request,'profile.html',{'user':user})

# @login_required
# def user_profile_edit(request):
    
    