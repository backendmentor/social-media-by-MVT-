from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Relationship(models.Model):
    from_user= models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    to_user= models.ForeignKey(User, on_delete=models.CASCADE, related_name="unfollower")
    created= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.from_user} following {self.to_user}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveSmallIntegerField(default=0)
    bio =models.TextField(blank=True, null=True)

