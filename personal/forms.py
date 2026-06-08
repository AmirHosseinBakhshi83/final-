# forms.py
from django import forms
from .models import Profile


class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField()

class ProfileForm(forms.ModelForm):
    """فرم ویرایش پروفایل کاربر"""
    
    class Meta:
        model = Profile
        fields = ['user_name', 'user_last', 'user_school', 'user_phone', 'user_info']

    def clean_user_phone(self):
        """اعتبارسنجی شماره تماس"""
        phone = self.cleaned_data.get('user_phone')
        if phone:
            phone_str = str(phone)
            if len(phone_str) != 10:
                raise forms.ValidationError('شماره تماس باید ۱۰ رقم باشد')
            if not phone_str.isdigit():
                raise forms.ValidationError('شماره تماس باید فقط شامل اعداد باشد')
        return phone

    def clean_user_name(self):
        """اعتبارسنجی نام"""
        name = self.cleaned_data.get('user_name')
        if name and len(name) < 2:
            raise forms.ValidationError('نام باید حداقل ۲ کاراکتر باشد')
        return name

    def clean_user_last(self):
        """اعتبارسنجی نام خانوادگی"""
        last = self.cleaned_data.get('user_last')
        if last and len(last) < 2:
            raise forms.ValidationError('نام خانوادگی باید حداقل ۲ کاراکتر باشد')
        return last