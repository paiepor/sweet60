from django.shortcuts import render, get_object_or_404
from jobs_app.models import JobListing

# หน้าแรกที่รวมงานทั้งหมด
def home(request):
    all_jobs = JobListing.objects.filter(is_active=True)
    return render(request, 'index.html', {'jobs': all_jobs})

# หน้าที่ดึงเฉพาะงานอันที่เรากดดู
def job_detail(request, job_id):
    job = get_object_or_404(JobListing, id=job_id)
    return render(request, 'job_detail.html', {'job': job})