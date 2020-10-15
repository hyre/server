from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from user.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

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
