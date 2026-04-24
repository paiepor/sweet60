from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    birthdate = models.DateField(null=True, blank=True, verbose_name="วันเกิด")
    experience = models.TextField(blank=True, verbose_name="ประสบการณ์ทำงาน")
    id_card_image = models.ImageField(upload_to='id_cards/', null=True, blank=True, verbose_name="รูปบัตรประชาชน")
    no_criminal_record = models.BooleanField(default=False, verbose_name="ยืนยันไม่มีประวัติอาชญากรรม")
    consent_id_upload = models.BooleanField(default=False, verbose_name="ยินยอมอัปโหลดบัตร")

    def __str__(self):
        return f"โปรไฟล์ของ {self.user.username}"


class Event(models.Model):
    title = models.CharField(max_length=200, verbose_name="ชื่อกิจกรรม")
    description = models.TextField(verbose_name="รายละเอียดกิจกรรม")
    start_time = models.DateTimeField(verbose_name="วันและเวลาเริ่มกิจกรรม")
    end_time = models.DateTimeField(verbose_name="วันและเวลาสิ้นสุดกิจกรรม", null=True, blank=True)
    location = models.CharField(max_length=255, verbose_name="สถานที่")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField(verbose_name="ข้อความ")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username}"

# ตารางที่ 2: เก็บข้อมูลงานที่เปิดรับสมัคร
class JobListing(models.Model):
    title = models.CharField(max_length=200, verbose_name="ชื่องาน")
    company_name = models.CharField(max_length=200, verbose_name="ชื่อบริษัท/ร้านค้า")
    description = models.TextField(verbose_name="รายละเอียดงาน")
    salary = models.CharField(max_length=100, verbose_name="เงินเดือน/ค่าจ้าง")
    is_active = models.BooleanField(default=True, verbose_name="ยังเปิดรับสมัครอยู่ไหม")
    
    # 1. ย้ายมาไว้ตรงนี้ 
    # 2. แก้เป็น on_delete (ไม่มีคำว่า server)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

class Application(models.Model):
    job = models.ForeignKey(JobListing, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.applicant.username} -> {self.job.title}"