from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created_at = models.DateField()
    updated_at = models.DateField()

    def __str__(self):
        return self.name


class Password(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="passwords")
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    service_name = models.CharField(max_length=255)
    encrypted_password = models.CharField(max_length=255)
    username_for_service = models.CharField(max_length=255)
    created_at = models.DateField()
    updated_at = models.DateField()

    def __str__(self):
        return self.service_name


class MasterPasswordHistory(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    old_hashed_password = models.CharField(max_length=255)
    changed_at = models.DateField()

    def __str__(self):
        return f"History for {self.user}"


class FailedLoginAttempts(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ip_address = models.CharField(max_length=255)
    attempt_time = models.DateField()
    was_successful = models.BooleanField()

    def __str__(self):
        return f"Failed login attempt for {self.user}"


class AuditLogs(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=255)
    action_description = models.CharField(max_length=255)
    created_at = models.DateField()

    def __str__(self):
        return f"Audit log for {self.user}"

class TwoFactorAuth(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_2fa_enabled = models.BooleanField()
    secret_key = models.CharField(max_length=255)
    backup_codes = models.CharField(max_length=255)

    def __str__(self):
        return f"2FA for {self.user}"

