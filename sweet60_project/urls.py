from django.contrib import admin
from django.urls import path
from . import views # ดึง views จากโฟลเดอร์เดียวกันมาใช้

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
]