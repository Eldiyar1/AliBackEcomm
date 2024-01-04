from django import forms
from django.contrib.auth.forms import (AuthenticationForm)  # PasswordResetForm, SetPasswordForm
from .models import Customer


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Имя пользователя', 'id': 'login-username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Пароль', 'id': 'login-pwd', }))


class RegistrationForm(forms.ModelForm):
    user_name = forms.CharField(min_length=4, max_length=50, label='Имя пользователя')
    email = forms.EmailField(max_length=100, label='Электронная почта')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Повторите пароль')

    class Meta:
        model = Customer
        fields = ('user_name', 'email',)

    def clean_user_name(self):
        user_name = self.cleaned_data['user_name'].lower()
        user = Customer.objects.filter(user_name=user_name)
        if user.count():
            raise forms.ValidationError("Такое имя пользователя уже существует")
        return user_name

    def clean_password2(self):
        data = self.cleaned_data
        if data['password'] != data['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return data['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if Customer.objects.filter(email=email).exists():
            raise forms.ValidationError('Используйте другой адрес электронной почты, этот уже занят')
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Имя пользователя'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Электронная почта', 'name': 'email', 'id': 'id_email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Пароль'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Повторите пароль'})

#
# class PwdResetForm(PasswordResetForm):
#     email = forms.EmailField(max_length=254, widget=forms.TextInput(
#         attrs={'class': 'form-control mb-3', 'placeholder': 'Электронная почта', 'id': 'form-email'}))
#
#     def clean_email(self):
#         email = self.cleaned_data['email']
#         u = Customer.objects.filter(email=email)
#         if not u:
#             raise forms.ValidationError(
#                 'К сожалению, мы не можем найти такой адрес электронной почты')
#         return email
#
#
# class PwdResetConfirmForm(SetPasswordForm):
#     new_password1 = forms.CharField(
#         label='Новый пароль', widget=forms.PasswordInput(
#             attrs={'class': 'form-control mb-3', 'placeholder': 'Новый пароль', 'id': 'form-newpass'}))
#     new_password2 = forms.CharField(
#         label='Повторите пароль', widget=forms.PasswordInput(
#             attrs={'class': 'form-control mb-3', 'placeholder': 'Повторите пароль', 'id': 'form-new-pass2'}))
#
#
# class UserEditForm(forms.ModelForm):
#     email = forms.EmailField(
#         label='Электронная почта (нельзя изменить)', max_length=200, widget=forms.TextInput(
#             attrs={'class': 'form-control mb-3', 'placeholder': 'Электронная почта', 'id': 'form-email',
#                    'readonly': 'readonly'}))
#     user_name = forms.CharField(
#         label='Имя пользователя', min_length=4, max_length=50, widget=forms.TextInput(
#             attrs={'class': 'form-control mb-3', 'placeholder': 'Имя пользователя', 'id': 'form-firstname',
#                    'readonly': 'readonly'}))
#     first_name = forms.CharField(
#         label='Имя', min_length=4, max_length=50, widget=forms.TextInput(
#             attrs={'class': 'form-control mb-3', 'placeholder': 'Имя', 'id': 'form-lastname'}))
#
#     class Meta:
#         model = Customer
#         fields = ('email', 'user_name', 'first_name',)
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['user_name'].required = True
#         self.fields['email'].required = True
