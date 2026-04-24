from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import JobListing, Profile

class JobForm(forms.ModelForm):
    class Meta:
        model = JobListing
        fields = ['title', 'company_name', 'description', 'salary']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full p-3 border rounded-xl mb-3', 'placeholder': 'เช่น พนักงานดูแลสวน'}),
            'company_name': forms.TextInput(attrs={'class': 'w-full p-3 border rounded-xl mb-3', 'placeholder': 'ชื่อร้านหรือบริษัท'}),
            'description': forms.Textarea(attrs={'class': 'w-full p-3 border rounded-xl mb-3', 'rows': 4, 'placeholder': 'รายละเอียดหน้าที่งาน...'}),
            'salary': forms.TextInput(attrs={'class': 'w-full p-3 border rounded-xl mb-3', 'placeholder': '12,000'}),
        }

class UserRegisterForm(UserCreationForm):
    full_name = forms.CharField(
        max_length=200, required=False, label="ชื่อ-นามสกุล",
        widget=forms.TextInput(attrs={'class': 'w-full p-3 border rounded-xl mb-3', 'placeholder': 'ระบุชื่อและนามสกุลจริง'})
    )
    email = forms.EmailField(
        required=True, label="อีเมล",
        widget=forms.EmailInput(attrs={'class': 'w-full p-3 border rounded-xl mb-3', 'placeholder': 'example@email.com'})
    )
    # เพิ่ม field สำหรับรูปโปรไฟล์ตรงนี้
    profile_image = forms.ImageField(
        required=False, label="รูปโปรไฟล์",
        widget=forms.FileInput(attrs={'class': 'mb-3'})
    )
    birthdate = forms.DateField(
        required=False, label="วัน/เดือน/ปีเกิด",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'w-full p-3 border rounded-xl mb-3'})
    )
    experience = forms.CharField(
        required=False, label="ประสบการณ์ทำงาน",
        widget=forms.Textarea(attrs={'rows': 4, 'class': 'w-full p-3 border rounded-xl mb-3', 'placeholder': 'บอกเล่าประสบการณ์หรืองานที่คุณเคยทำ...'})
    )
    id_card_image = forms.ImageField(required=False, label="รูปบัตรประชาชน")

    class Meta(UserCreationForm.Meta):
        model = User
        # ระบุ fields ที่จะดึงมาจาก User Model หลัก
        fields = ['username', 'email', 'full_name'] 

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'w-full p-4 bg-gray-50 rounded-2xl border-none text-sm'}),
            'email': forms.EmailInput(attrs={'class': 'w-full p-4 bg-gray-50 rounded-2xl border-none text-sm'}),
            'first_name': forms.TextInput(attrs={'class': 'w-full p-4 bg-gray-50 rounded-2xl border-none text-sm'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full p-4 bg-gray-50 rounded-2xl border-none text-sm'}),
        }

# ฟอร์มสำหรับอัปเดตรูปโปรไฟล์โดยเฉพาะ
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'birthdate', 'experience']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'mb-3'}),
            'birthdate': forms.DateInput(attrs={'type': 'date', 'class': 'w-full p-3 border rounded-xl mb-3'}),
            'experience': forms.Textarea(attrs={'rows': 4, 'class': 'w-full p-3 border rounded-xl mb-3'}),
        }
        