from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from jobs_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('register/', views.register_view, name='register'),
    path('health/', lambda request: HttpResponse('ok'), name='health'),
    path('setup-admin/', views.setup_admin, name='setup_admin'),
    path('', views.landing, name='landing'),
    path('home/', views.index, name='home'),
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
    path('jobs/', views.jobs_list, name='jobs_list'),
    path('create-job/', views.create_job, name='create_job'),
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('profile/', views.profile_page, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('events/', views.events_list, name='events_list'),
    path('emergency/', views.emergency_page, name='emergency'),
    path('community/', views.community_page, name='community'),
    path('groups/', views.my_groups, name='my_groups'),
    path('groups/create/', views.create_group, name='create_group'),
    path('groups/<int:group_id>/', views.group_detail, name='group_detail'),
    path('chat/<int:user_id>/', views.chat_room, name='chat_room'),
    path('chat/start/<int:job_id>/', views.start_chat, name='start_chat'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
