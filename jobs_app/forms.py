from django import forms
from .models import JobListing

class JobForm(forms.ModelForm):
    class Meta:
        model = JobListing
        # ฟีลด์ที่จะให้คนโพสต์งานกรอก
        fields = ['title', 'company_name', 'description', 'salary']
        
        # ใส่ CSS (Tailwind) ให้ช่องกรอกดูสวยเหมือนแอปที่คุณออกแบบไว้
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full p-3 border rounded-xl mb-3', 'placeholder': 'เช่น พนักงานดูแลสวน'}),
            'company_name': forms.TextInput(attrs={'class': 'w-full p-3 border rounded-xl mb-3', 'placeholder': 'ชื่อร้านหรือบริษัท'}),
            'description': forms.Textarea(attrs={'class': 'w-full p-3 border rounded-xl mb-3', 'rows': 4, 'placeholder': 'รายละเอียดหน้าที่งาน...'}),
            'salary': forms.TextInput(attrs={'class': 'w-full p-3 border rounded-xl mb-3', 'placeholder': '12,000'}),
        }
    
from django.contrib.auth.models import User

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        # ใส่สไตล์ให้สวยเหมือนช่องลงประกาศงาน
        widgets = {
            'username': forms.TextInput(attrs={'class': 'w-full p-4 bg-gray-50 rounded-2xl border-none text-sm'}),
            'email': forms.EmailInput(attrs={'class': 'w-full p-4 bg-gray-50 rounded-2xl border-none text-sm'}),
            'first_name': forms.TextInput(attrs={'class': 'w-full p-4 bg-gray-50 rounded-2xl border-none text-sm'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full p-4 bg-gray-50 rounded-2xl border-none text-sm'}),
        }