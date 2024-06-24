# Generated by Django 4.2 on 2024-06-23 14:33

import accounts.models
import core.validators
from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, validators=[core.validators.alpha_validator])),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=13, region=None)),
                ('avatar', models.ImageField(blank=True, default=accounts.models.Account.default_directory_path, upload_to=accounts.models.Account.directory_path)),
                ('description', models.TextField(blank=True, null=True)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('locale', models.CharField(choices=[('en', 'English'), ('ar', 'Arabic'), ('fr', 'French')], default='en', max_length=255)),
                ('theme', models.CharField(choices=[('light', 'Light'), ('dark', 'Dark')], default='light', max_length=255)),
                ('country', models.CharField(choices=[('DZ', 'Algeria')], default='DZ', max_length=255)),
                ('transactions_count', models.PositiveIntegerField(blank=True, default=0)),
                ('chargily_id', models.CharField(blank=True, max_length=255, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
