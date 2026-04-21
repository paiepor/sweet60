from django.contrib import admin
from django.urls import path
from jobs_app import views  # 1. แก้ไขให้ Import มาจากแอป jobs_app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'), # 2. หน้าแรกให้เรียกไปที่ views.index
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
    
    # 3. เพิ่มเส้นทางสำหรับหน้าลงประกาศงานและสมัครงาน
    path('create-job/', views.create_job, name='create_job'),
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('profile/', views.profile_page, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]