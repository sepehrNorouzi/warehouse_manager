# Generated by Django 5.0.4 on 2024-04-22 11:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Company name')),
                ('phone', models.CharField(blank=True, max_length=100, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format:+989999999999' or '99999999999'.Up to 13 digits allowed.allowed characters: [0-9] and '+'.", regex='^((?:[0-9]{8,10})|(?:\\+[0-9][0-9]{11,14}))$')], verbose_name='Company phone')),
                ('address', models.TextField(blank=True, null=True, verbose_name='Company address')),
            ],
            options={
                'verbose_name': 'Company',
                'verbose_name_plural': 'Companies',
            },
        ),
    ]
