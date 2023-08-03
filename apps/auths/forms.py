import re
from datetime import timedelta,datetime

#Django
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.forms import AuthenticationForm

#Local
from .models import CustomUser


class CustomUserForm(forms.ModelForm):
    """
    CustomUserForm.
    """

    email = forms.EmailField(
        max_length=254,
        label='Почта'
    )
    password = forms.CharField(
        widget=forms.PasswordInput, 
        label='Пароль'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput, 
        label='Подтвердите пароль'
    )
    nickname = forms.CharField(min_length=2,max_length=69,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-zА-Яа-я][A-Za-zА-Яа-я]{2,}$',
                message="Никнейм может состоять лишь из буквенных символов."
            )
        ],
        
        label='Имя'
    )

    class Meta:
        model = CustomUser
        fields = ['email', 'nickname', 'password', 'password2']

    def save(self, commit: bool = ...) -> CustomUser:
        self.full_clean()
        return super().save(commit)