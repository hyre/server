from django.shortcuts import render, HttpResponse

def dashboard(request,username):
    print(username)
    return render(request, 'hrdash.html')
