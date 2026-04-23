from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import JobListing, Application
from .forms import JobForm, UserUpdateForm


def index(request):
    jobs = JobListing.objects.filter(is_active=True).order_by('-id')
    return render(request, 'index.html', {'jobs': jobs})


def job_detail(request, job_id):
    job = get_object_or_404(JobListing, id=job_id)
    return render(request, 'job_detail.html', {'job': job})


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
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


@login_required
def apply_job(request, job_id):
    if request.method == 'POST':
        job = get_object_or_404(JobListing, id=job_id)
        Application.objects.create(job=job, applicant=request.user)
    return redirect('job_detail', job_id=job_id)


@login_required
def profile_page(request):
    my_posts = JobListing.objects.filter(author=request.user)
    my_apps = Application.objects.filter(applicant=request.user)
    return render(request, 'profile.html', {
        'my_posts': my_posts,
        'my_apps': my_apps
    })


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})
