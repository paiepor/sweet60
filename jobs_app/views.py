from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import JobListing, Application, UserProfile, Event, ChatMessage
from .forms import JobForm, UserUpdateForm, UserRegisterForm
from django.contrib.auth.models import User
from django.db.models import Q


def landing(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'landing.html')


def index(request):
    events = Event.objects.all().order_by('-start_time')[:3]
    return render(request, 'index.html', {'events': events})


def events_list(request):
    events = Event.objects.all().order_by('-start_time')
    return render(request, 'events.html', {'events': events})


def emergency_page(request):
    return render(request, 'emergency.html')


def jobs_list(request):
    query = request.GET.get('q', '').strip()
    jobs = JobListing.objects.filter(is_active=True).order_by('-id')
    if query:
        jobs = (jobs.filter(title__icontains=query) | JobListing.objects.filter(is_active=True, company_name__icontains=query)).distinct().order_by('-id')
    return render(request, 'jobs.html', {'jobs': jobs, 'query': query})


def job_detail(request, job_id):
    job = get_object_or_404(JobListing, id=job_id)
    return render(request, 'job_detail.html', {'job': job})


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            full_name = form.cleaned_data.get('full_name', '').strip()
            parts = full_name.split(' ', 1)
            user.first_name = parts[0]
            user.last_name = parts[1] if len(parts) > 1 else ''
            user.email = form.cleaned_data.get('email', '')
            user.save()
            UserProfile.objects.create(
                user=user,
                birthdate=form.cleaned_data.get('birthdate'),
                experience=form.cleaned_data.get('experience', ''),
                id_card_image=form.cleaned_data.get('id_card_image'),
                no_criminal_record='no_criminal_record' in request.POST,
                consent_id_upload='consent_id_upload' in request.POST,
            )
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
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
def community_page(request):
    # Retrieve users the current user has chatted with
    sent_to = ChatMessage.objects.filter(sender=request.user).values_list('receiver', flat=True)
    received_from = ChatMessage.objects.filter(receiver=request.user).values_list('sender', flat=True)
    chat_user_ids = set(list(sent_to) + list(received_from))
    
    chat_users = User.objects.filter(id__in=chat_user_ids)
    
    # Optional: Attach last message for preview
    for u in chat_users:
        last_msg = ChatMessage.objects.filter(
            Q(sender=request.user, receiver=u) | Q(sender=u, receiver=request.user)
        ).order_by('-timestamp').first()
        u.last_message = last_msg

    return render(request, 'community.html', {'chat_users': chat_users})


@login_required
def chat_room(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            ChatMessage.objects.create(sender=request.user, receiver=other_user, content=content)
            return redirect('chat_room', user_id=other_user.id)
            
    messages = ChatMessage.objects.filter(
        Q(sender=request.user, receiver=other_user) | Q(sender=other_user, receiver=request.user)
    ).order_by('timestamp')
    
    return render(request, 'chat_room.html', {'other_user': other_user, 'messages': messages})


@login_required
def start_chat(request, job_id):
    job = get_object_or_404(JobListing, id=job_id)
    # Start a chat with the job author
    return redirect('chat_room', user_id=job.author.id)


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
