# Generated by Django 3.2.23 on 2024-01-13 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitepanel', '0004_alter_userprofile_otp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_type',
            field=models.CharField(choices=[('ORGANISATION', 'Organisation'), ('USER', 'User')], default='unassigned', max_length=30),
        ),
    ]
