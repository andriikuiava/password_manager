# Generated by Django 4.2.16 on 2024-11-17 11:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('password_manager', '0004_user_groups_user_is_active_user_is_staff_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SessionData',
        ),
    ]
