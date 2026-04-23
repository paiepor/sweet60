from django.contrib import admin
from django.urls import path, include
from jobs_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register_view, name='register'),
    path('', views.index, name='home'),
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
    path('create-job/', views.create_job, name='create_job'),
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('profile/', views.profile_page, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]
