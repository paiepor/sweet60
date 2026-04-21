from django.contrib import admin
from .models import ElderlyProfile, JobListing

# นำตารางไปลงทะเบียนโชว์ในหน้าแอดมิน
admin.site.register(ElderlyProfile)
admin.site.register(JobListing)