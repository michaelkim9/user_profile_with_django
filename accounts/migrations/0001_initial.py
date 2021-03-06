# Generated by Django 2.0 on 2018-01-19 22:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('bio', tinymce.models.HTMLField(blank=True)),
                ('avatar', models.ImageField(blank=True, upload_to='avatars/')),
                ('city', models.CharField(blank=True, max_length=100)),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2)),
                ('hobby', models.CharField(blank=True, max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
