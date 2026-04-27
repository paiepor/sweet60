import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import JobListing, Application, UserProfile, Event, ChatMessage, CommunityGroup, GroupPost, GroupPostLike
from .forms import JobForm, UserUpdateForm, UserRegisterForm, CommunityGroupForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.urls import reverse
import base64, io
from PIL import Image


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
        context['unread_count'] = context['msg_count']
    return render(request, 'index.html', context)


def events_list(request):
    events = Event.objects.all().order_by('-start_time')
    return render(request, 'events.html', {'events': events})


def emergency_page(request):
    return render(request, 'emergency.html')

# โค้ดเก่า
# def jobs_list(request):
#     query = request.GET.get('q', '').strip()
#     jobs = JobListing.objects.filter(is_active=True).order_by('-id')
#     if query:
#         jobs = (jobs.filter(title__icontains=query) | JobListing.objects.filter(is_active=True, company_name__icontains=query)).distinct().order_by('-id')
#     return render(request, 'jobs.html', {'jobs': jobs, 'query': query})

def jobs_list(request):
    query = request.GET.get('q', '').strip()
    jobs = JobListing.objects.filter(is_active=True).order_by('-id')
    if query:
        jobs = (jobs.filter(title__icontains=query) | JobListing.objects.filter(is_active=True, company_name__icontains=query)).distinct().order_by('-id')
    applied_job_ids = set()
    if request.user.is_authenticated:
        applied_job_ids = set(Application.objects.filter(applicant=request.user).values_list('job_id', flat=True))
    return render(request, 'jobs.html', {'jobs': jobs, 'query': query, 'applied_job_ids': applied_job_ids})

# โค้ดเก่า
# def job_detail(request, job_id):
#     job = get_object_or_404(JobListing, id=job_id)
#     return render(request, 'job_detail.html', {'job': job})

# โค้ดใหม่
def job_detail(request, job_id):
    job = get_object_or_404(JobListing, id=job_id)
    already_applied = False
    if request.user.is_authenticated:
        already_applied = Application.objects.filter(job=job, applicant=request.user).exists()
    return render(request, 'job_detail.html', {'job': job, 'already_applied': already_applied})

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
            avatar_b64 = request.POST.get('avatar_b64', '')
            UserProfile.objects.create(
                user=user,
                birthdate=form.cleaned_data.get('birthdate'),
                experience=form.cleaned_data.get('experience', ''),
                id_card_image=form.cleaned_data.get('id_card_image'),
                no_criminal_record='no_criminal_record' in request.POST,
                consent_id_upload='consent_id_upload' in request.POST,
                avatar_b64=avatar_b64,
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


# @login_required
# def apply_job(request, job_id):
#     if request.method == 'POST':
#         job = get_object_or_404(JobListing, id=job_id)
#         Application.objects.create(job=job, applicant=request.user)
#     return redirect('job_detail', job_id=job_id)

@login_required
def apply_job(request, job_id):
    if request.method == 'POST':
        job = get_object_or_404(JobListing, id=job_id)
        already_applied = Application.objects.filter(job=job, applicant=request.user).exists()
        if not already_applied:
            Application.objects.create(job=job, applicant=request.user)
    return redirect(reverse('profile') + '#applications')

@login_required
def profile_page(request):
    my_posts = JobListing.objects.filter(author=request.user).order_by('-id')
    my_apps = Application.objects.filter(applicant=request.user).select_related('job').order_by('-applied_at')
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'profile.html', {
        'my_posts': my_posts,
        'my_apps': my_apps,
        'profile': profile,
    })


@login_required
def edit_job(request, job_id):
    job = get_object_or_404(JobListing, id=job_id, author=request.user)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = JobForm(instance=job)
    return render(request, 'edit_job.html', {'form': form, 'job': job})


@login_required
def community_page(request):
    query = request.GET.get('q', '').strip()
    sent_to = ChatMessage.objects.filter(sender=request.user).values_list('receiver', flat=True)
    received_from = ChatMessage.objects.filter(receiver=request.user).values_list('sender', flat=True)
    chat_user_ids = set(list(sent_to) + list(received_from))
    chat_users = User.objects.filter(id__in=chat_user_ids)
    if query:
        chat_users = chat_users.filter(
            Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query)
        )
    chat_user_list = list(chat_users)
    avatar_map = {p.user_id: p.avatar_b64 for p in UserProfile.objects.filter(user_id__in=[u.id for u in chat_user_list])}
    for u in chat_user_list:
        last_msg = ChatMessage.objects.filter(
            Q(sender=request.user, receiver=u) | Q(sender=u, receiver=request.user)
        ).order_by('-timestamp').first()
        u.last_message = last_msg
        u.avatar_b64 = avatar_map.get(u.id, '')
    unread_count = ChatMessage.objects.filter(receiver=request.user).count()
    return render(request, 'community.html', {
        'chat_users': chat_user_list,
        'query': query,
        'unread_count': unread_count,
    })


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
    other_profile = UserProfile.objects.filter(user=other_user).first()
    other_avatar = other_profile.avatar_b64 if other_profile else ''
    return render(request, 'chat_room.html', {'other_user': other_user, 'messages': messages, 'other_avatar': other_avatar})


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

    posts = list(group.posts.select_related('author').prefetch_related('likes').order_by('-created_at'))
    liked_ids = set(GroupPostLike.objects.filter(user=request.user, post__group=group).values_list('post_id', flat=True))
    author_ids = {post.author_id for post in posts}
    avatar_map = {p.user_id: p.avatar_b64 for p in UserProfile.objects.filter(user_id__in=author_ids)}
    for post in posts:
        post.liked_by_user = post.id in liked_ids
        post.like_count_val = post.likes.count()
        post.author_avatar = avatar_map.get(post.author_id, '')

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

def explore_groups2(request):
    groups = CommunityGroup.objects.filter(is_private=False).order_by('-created_at')
    return render(request, 'explore_groups2.html', {'groups': groups})

@login_required
def create_group(request):
    if request.method == 'POST':
        form = CommunityGroupForm(request.POST, request.FILES)
        if form.is_valid():
            group = form.save(commit=False)
            group.creator = request.user
            cover_file = request.FILES.get('cover_image')
            if cover_file:
                img = Image.open(cover_file)
                img.thumbnail((800, 400))
                if img.mode in ('RGBA', 'P', 'LA'):
                    img = img.convert('RGB')
                buf = io.BytesIO()
                img.save(buf, format='JPEG', quality=82)
                group.cover_image_b64 = 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()
            group.save()
            group.members.add(request.user)
            return redirect('my_groups')
    else:
        form = CommunityGroupForm()
    return render(request, 'create_group.html', {'form': form})


@login_required
def clear_avatar(request):
    if request.method == 'POST':
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        profile.avatar_b64 = ''
        profile.save()
    return redirect('edit_profile')


@login_required
def delete_job(request, job_id):
    if request.method == 'POST':
        job = get_object_or_404(JobListing, id=job_id, author=request.user)
        job.delete()
    return redirect('profile')


@login_required
def delete_group_post(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(GroupPost, id=post_id)
        group_id = post.group.id
        if post.author == request.user or post.group.creator == request.user:
            post.delete()
        return redirect('group_detail', group_id=group_id)
    return redirect('community')


@login_required
def help_center(request):
    return render(request, 'help.html')


@login_required
def support_chat(request):
    return render(request, 'support_chat.html')


@login_required
def edit_profile(request):
    import base64, io
    from PIL import Image
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            avatar_file = request.FILES.get('avatar')
            if avatar_file:
                img = Image.open(avatar_file)
                img.thumbnail((300, 300))
                if img.mode in ('RGBA', 'P', 'LA'):
                    img = img.convert('RGB')
                buf = io.BytesIO()
                img.save(buf, format='JPEG', quality=82)
                profile.avatar_b64 = 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()
                profile.save()
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form, 'profile': profile})
