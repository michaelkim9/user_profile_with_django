from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField
from tinymce.models import HTMLField


# Profile model using Django's built-in user model
class Profile(models.Model):
    user = models.OneToOneField(User,
                                related_name='profile',
                                on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    bio = HTMLField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    city = models.CharField(blank=True, max_length=100)
    country = CountryField(blank=True)
    hobby = models.CharField(max_length=100, blank=True)

# Signal methods to create and save profiles once User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
