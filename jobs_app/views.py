from django.shortcuts import render, redirect, get_object_or_404
from .models import JobListing, Application
from .forms import JobForm

# 1. หน้าแรก
def index(request):
    jobs = JobListing.objects.filter(is_active=True).order_by('-id')
    return render(request, 'index.html', {'jobs': jobs})

# 2. หน้ารายละเอียดงาน
def job_detail(request, job_id):
    job = get_object_or_404(JobListing, id=job_id)
    return render(request, 'job_detail.html', {'job': job})

# 3. หน้าลงประกาศงาน
def create_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.author = request.user
            job.save()
            return redirect('home')
    else:
        form = JobForm()
    return render(request, 'create_job.html', {'form': form})

# 4. ฟังก์ชันกดสมัครงาน
def apply_job(request, job_id):
    if request.method == 'POST':
        job = get_object_or_404(JobListing, id=job_id)
        Application.objects.create(job=job, applicant=request.user)
        return redirect('home')
    
def profile_page(request):
    # ดึงข้อมูลงานที่เราโพสต์เอง และงานที่เราไปสมัครไว้มาโชว์
    my_posts = JobListing.objects.filter(author=request.user)
    my_apps = Application.objects.filter(applicant=request.user)
    
    return render(request, 'profile.html', {
        'my_posts': my_posts,
        'my_apps': my_apps
    })

from .forms import UserUpdateForm # อย่าลืม import เพิ่มด้านบนด้วยนะ

def edit_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile') # เซฟเสร็จกลับไปหน้าโปรไฟล์
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})