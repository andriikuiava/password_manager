# Generated by Django 4.2.16 on 2024-11-30 17:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('password_manager', '0008_user_encryption_key'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='encryption_key',
        ),
    ]
