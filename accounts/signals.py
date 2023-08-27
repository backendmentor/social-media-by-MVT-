from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Profile

def creat_profile (sender, **kwargs):
    if kwargs["created"]:
        Profile.objects.create(user=kwargs['instance'])

post_save.connect(receiver= creat_profile , sender=User)