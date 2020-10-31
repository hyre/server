from django.shortcuts import render, HttpResponse
from company.forms import JobForm
from company.models import HR_bio, Application,Job
from django.contrib.auth.decorators import login_required
from user.models import Dev, Skill

@login_required
def dashboard(request,username):
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

@login_required
def post_jobs(request):
    if(request.method=='POST'):
        form = JobForm(request.POST)
        if(form.is_valid):
            form.save()
            return HttpResponse("Created")
    company = HR_bio.objects.all().filter(user=request.user)[0].works_for
    form = JobForm(initial={'company':company,'posted_by':request.user})
    return render(request,'create_job.html',{'form':form})


@login_required
def posted_jobs(request):
    jobs = Job.objects.all().filter(posted_by=request.user)
    return render(request,'posted_jobs.html',{'jobs':jobs})

def view_applications(request,id):
    job = Job.objects.all().filter(id=id)
    applications = Application.objects.all().filter(job_name=job[0])
    return render(request,'applied_devs.html',{'applications':applications})

