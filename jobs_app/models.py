from django.db import models

# ตารางที่ 1: เก็บข้อมูลประวัติผู้สูงอายุที่มาสมัครงาน
class ElderlyProfile(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="ชื่อจริง")
    last_name = models.CharField(max_length=100, verbose_name="นามสกุล")
    age = models.IntegerField(verbose_name="อายุ")
    skills = models.TextField(verbose_name="ทักษะ/ความสามารถ")
    experience = models.TextField(verbose_name="ประสบการณ์ทำงานที่ผ่านมา")
    phone_number = models.CharField(max_length=15, verbose_name="เบอร์โทรศัพท์")

    def __str__(self):
        return f"{self.first_name} {self.last_name} (อายุ {self.age} ปี)"

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