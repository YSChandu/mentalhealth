from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link each conversation to a user
    user_input = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation with {self.user.username} at {self.timestamp}"

class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)  # Optional field
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)  # Optional field
    nationality = models.CharField(max_length=50, blank=True, null=True)  # Optional field

    def __str__(self):
        return self.user.username

# Signal to automatically create Profile when a User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


