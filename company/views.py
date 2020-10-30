from django.shortcuts import render, HttpResponse
from company.forms import JobForm
from company.models import HR_bio
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request,username):
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