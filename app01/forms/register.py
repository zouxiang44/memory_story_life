from django import forms
from django.core.validators import RegexValidator
from app01.models import Person


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=3, required=True, label='用户名', error_messages={
        'required': '此项必填',
        'max_length': '长度过长', })

    password = forms.CharField(max_length=10, min_length=8, required=True, label='密码', error_messages={
        'min_length': '长度过短',
        'max_length': '长度过长',
        'required': '此项必填', })

    password_again = forms.CharField(max_length=10, min_length=8, required=True, label='再次输入密码', error_messages={
        'min_length': '长度过短',
        'max_length': '长度过长',
        'required': '此项必填', })

    email = forms.EmailField(label='邮箱', required=False, error_messages={
        'invalid': '邮箱格式不对',
    }, widget=forms.TextInput(attrs={
        'placeholder': '此项可不填'}))

    phone = forms.CharField(label='电话', required=False, widget=forms.TextInput(attrs={
        'placeholder': '此项可不填',
    }), validators=[
        RegexValidator(r'\d+', '请输入数字'),
        RegexValidator(r'1[3-9]\d{9}', '手机号格式不对'),])

    def clean(self):
        is_service = Person.objects.filter(
            username=self.cleaned_data.get('username'),
        ).exists()
        if is_service:
            self.add_error('username', '用户已存在')
        password = self.cleaned_data.get('password')
        password_again = self.cleaned_data.get('password_again')
        if password != password_again:
            self.add_error('password_again', '两次密码不一致')
        return self.cleaned_data
