# forms.py in your accounts app
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField
from personal.models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user_name', 'user_last', 'user_school', 'user_phone']
        widgets = {
            'user_name': forms.TextInput(attrs={'placeholder': 'نام خود را وارد کنید'}),
            'user_last': forms.TextInput(attrs={'placeholder': 'نام خانوادگی خود را وارد کنید'}),
            'user_school': forms.TextInput(attrs={'placeholder': 'نام مدرسه یا دانشگاه خود را وارد کنید'}),
            'user_phone': forms.TextInput(attrs={'placeholder': '09120000000'}),
        }


class CustomUserCreationForm(UserCreationForm):
    captcha = CaptchaField(label='Verification Code')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')