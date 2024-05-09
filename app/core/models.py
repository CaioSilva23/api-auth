"""
Database models.
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"


class Profile(models.Model):
    """Model profile"""
    about = models.TextField(null=True, blank=True)
    office = models.CharField(max_length=255, null=True, blank=True)
    photograph = models.ImageField(upload_to='profile/photograph/',
                                   blank=True,
                                   null=True,
                                   )
    curriculum = models.FileField(upload_to='profile/curriculum/')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        """Meta definition for MODELNAME."""

        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return self.user.name

    def name(self):
        return self.user.name

    def email(self):
        return self.user.email
