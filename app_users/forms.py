from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm


class AuthForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_username(self):
        username = self.cleaned_data.get("username")
        user_qs = User.objects.filter(username=username)
        if user_qs.count() == 0:
            raise forms.ValidationError("Коричтувача не знайдено")
        return username
    # def clean(self, *args, **kwargs):
    #     username = self.cleaned_data.get("username")
    #     password = self.cleaned_data.get("password")
    #     user_qs = User.objects.filter(username=username)
    #     user = User.objects.get(username=username)
    #
    #     if user_qs.count() == 0:
    #         raise forms.ValidationError("Коричтувача не знайдено")
    #     # elif not user.check_password(password):
    #     #     raise forms.ValidationError("Некоректний пароль")
    #     # else:
    #     #     user = authenticate(request, username=self.cleaned_data['username'],
    #     #                         password=self.cleaned_data['password'])
    #     #     user.backend = 'django.contrib.auth.backends.ModelBackend'
    #     #     login(request, user)
    #     return username, password


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ("username", "email", "password1",)

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('Ця електронна скринька вже зареєстрована!')
        return email


class ChangePassUserForm(UserCreationForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('password1',)


class ChangeUserStatusForm(ModelForm):
    class Meta:
        model = User
        fields = ('is_active', 'is_staff', 'is_superuser')
