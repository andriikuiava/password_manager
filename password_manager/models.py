from django.db import models


class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.username


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


class TwoFactorAuth(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_2fa_enabled = models.BooleanField()
    secret_key = models.CharField(max_length=255)
    backup_codes = models.CharField(max_length=255)

    def __str__(self):
        return f"2FA for {self.user}"


class SessionData(models.Model):
    session_key = models.BigIntegerField(primary_key=True)
    session_data = models.CharField(max_length=255)
    expire_date = models.DateField()

    def __str__(self):
        return f"Session {self.session_key}"
