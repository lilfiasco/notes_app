#Django
from django.db import models
from django.contrib.auth.base_user import (
    AbstractBaseUser,
    BaseUserManager,
)
from django.utils import timezone
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import PermissionsMixin


class CustomUserManager(BaseUserManager):
    """Custom User Manager."""

    def create_user(self, email, password):
        if not email:
            raise ValidationError('email is required')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Custom User model."""
    email = models.EmailField(
        verbose_name='почта',
        unique=True
    )
    nickname = models.CharField(
        max_length=150,
        verbose_name='никнейм',
        blank=True,
        null=True
    )
    is_superuser = models.BooleanField(
        verbose_name='Superuser',
        default=False
    )
    is_active = models.BooleanField(
        verbose_name='Active',
        default=True
    )
    is_staff = models.BooleanField(
        verbose_name='Staff',
        default=False
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:

        ordering = ('-id',)
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    # def save(self, *args, **kwargs):
    #     self.full_clean()
    #     return super().save(*args, **kwargs)
    
