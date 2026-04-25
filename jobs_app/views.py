import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import JobListing, Application, UserProfile, Event, ChatMessage, CommunityGroup, GroupPost, GroupPostLike
from .forms import JobForm, UserUpdateForm, UserRegisterForm, CommunityGroupForm
from django.contrib.auth.models import User
from django.db.models import Q


def setup_admin(request):
    from django.http import HttpResponse
    if User.objects.filter(is_superuser=True).exists():
        return HttpResponse('Admin already exists.')
    username = os.environ.get('ADMIN_USERNAME', 'admin')
    password = os.environ.get('ADMIN_PASSWORD')
    email = os.environ.get('ADMIN_EMAIL', '')
    if not password:
        return HttpResponse('ADMIN_PASSWORD not set.')
    User.objects.create_superuser(username=username, email=email, password=password)
    return HttpResponse(f'Superuser "{username}" created successfully.')


def landing(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'landing.html')


def index(request):
    from django.utils import timezone
    recent_jobs = JobListing.objects.filter(is_active=True).order_by('-id')[:3]
    upcoming_events = Event.objects.filter(start_time__gte=timezone.now()).order_by('start_time')[:2]
    context = {
        'recent_jobs': recent_jobs,
        'upcoming_events': upcoming_events,
    }
    if request.user.is_authenticated:
        context['app_count'] = Application.objects.filter(applicant=request.user).count()
        context['msg_count'] = ChatMessage.objects.filter(receiver=request.user).count()
    return render(request, 'index.html', context)


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
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
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
def my_groups(request):
    groups = CommunityGroup.objects.filter(members=request.user).order_by('-created_at')
    return render(request, 'my_groups.html', {'groups': groups})


@login_required
def group_detail(request, group_id):
    group = get_object_or_404(CommunityGroup, id=group_id)
    is_member = group.members.filter(id=request.user.id).exists()

    if request.method == 'POST':
        if is_member:
            content = request.POST.get('content', '').strip()
            image = request.FILES.get('image')
            if content or image:
                GroupPost.objects.create(group=group, author=request.user, content=content, image=image)
        return redirect('group_detail', group_id=group_id)

    posts = group.posts.select_related('author').prefetch_related('likes').order_by('-created_at')
    liked_ids = set(GroupPostLike.objects.filter(user=request.user, post__group=group).values_list('post_id', flat=True))
    for post in posts:
        post.liked_by_user = post.id in liked_ids
        post.like_count_val = post.likes.count()

    return render(request, 'group_detail.html', {'group': group, 'posts': posts, 'is_member': is_member})


@login_required
def like_post(request, post_id):
    post = get_object_or_404(GroupPost, id=post_id)
    like, created = GroupPostLike.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
    return redirect('group_detail', group_id=post.group.id)


@login_required
def join_group(request, group_id):
    group = get_object_or_404(CommunityGroup, id=group_id)
    if group.members.filter(id=request.user.id).exists():
        group.members.remove(request.user)
    else:
        group.members.add(request.user)
    return redirect('group_detail', group_id=group_id)


def explore_groups(request):
    groups = CommunityGroup.objects.filter(is_private=False).order_by('-created_at')
    return render(request, 'explore_groups.html', {'groups': groups})


@login_required
def create_group(request):
    if request.method == 'POST':
        form = CommunityGroupForm(request.POST, request.FILES)
        if form.is_valid():
            group = form.save(commit=False)
            group.creator = request.user
            group.save()
            group.members.add(request.user)
            return redirect('community')
    else:
        form = CommunityGroupForm()
    return render(request, 'create_group.html', {'form': form})


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
