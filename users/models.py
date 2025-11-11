from django.contrib.auth.models import AbstractUser
from django.db import models

from .manager import CustomUserManager


class User(AbstractUser):
    AUTH_PROVIDER_CHOICES = (
        ("google", "Google"),
        ("email", "Email"),
    )

    username = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField("email address", unique=True)
    auth_provider = models.CharField(max_length=10, choices=AUTH_PROVIDER_CHOICES, default="email")
    is_verify = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if not self.pk:  # Only execute this code when creating a new user
            password = self.password
            print(self.password)
            if len(password) < 40:
                self.set_password(password)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = verbose_name_plural = "Users"

    def __str__(self):
        return self.email


class EmailVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verification_token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email
