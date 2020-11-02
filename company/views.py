from django.shortcuts import render, HttpResponse
from company.forms import JobForm
from company.models import HR_bio, Application,Job
from django.contrib.auth.decorators import login_required
from user.models import Dev, Skill

@login_required
def dashboard(request,username):
    if(request.user.type=='HR'):
        if(request.method=="POST"):
            query = request.POST['search']
            dev = Dev.objects.all().filter(username=query)
            res = Skill.objects.all()
            usernames = []
            for i in res:
                if(query in i.skill_string.split(',')):
                    usernames.append(i.user.username)
            print(usernames)
            return render(request,'hrdash.html',{'dev':dev,'usernames':usernames})
        return render(request, 'hrdash.html')
    else:
        return render(request,'404.html')

@login_required
def post_jobs(request):
    if(request.user.type=='HR'):
        if(request.method=='POST'):
            form = JobForm(request.POST)
            if(form.is_valid):
                form.save()
                return render(request,'application.html',{'message':'Job posting has been created!'})
        company = HR_bio.objects.all().filter(user=request.user)[0].works_for
        form = JobForm(initial={'company':company,'posted_by':request.user})
        return render(request,'create_job.html',{'form':form})
    else:
        return render(request,'404.html')


@login_required
def posted_jobs(request):
    if(request.user.type=='HR'):
        jobs = Job.objects.all().filter(posted_by=request.user)
        return render(request,'posted_jobs.html',{'jobs':jobs})
    else:
        return render(request,'404.html')

@login_required
def view_applications(request,id):
    if(request.user.type=='HR'):
        job = Job.objects.all().filter(id=id)
        applications = Application.objects.all().filter(job_name=job[0])
        return render(request,'applied_devs.html',{'applications':applications,'job':job[0]})
    else:
        render(request,'404.html')

