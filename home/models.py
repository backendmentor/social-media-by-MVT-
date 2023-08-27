from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse

class POST(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE, related_name="posts")
    title=models.CharField(max_length=200)
    content=models.TextField()
    image=models.ImageField(upload_to="post/", null=True, blank=True)
    slug=models.SlugField()
    created_data= models.DateTimeField(auto_now_add=True)
    update_data=models.DateTimeField(auto_now=True)


    class Meta:
        ordering =( "-created_data", )

    def __str__(self):
        return f'{self.user.username} : {self.content[:20]}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("home:post_detail", args=(self.id, self.slug))

    def count_likes(self):
        return self.post_likes.count()


class Comment(models.Model):
    post= models.ForeignKey(POST, on_delete=models.CASCADE , related_name="post_comment")
    user=models.ForeignKey(User,on_delete=models.CASCADE, related_name="user_comment")
    reply=models.ForeignKey("self",on_delete=models.CASCADE, related_name="reply_comment", null=True, blank=True )
    is_reply= models.BooleanField(default=False)
    content=models.TextField(max_length=200)
    created_data=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.content[:20]}"


class Postlikes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE , related_name="user_likes")
    post= models.ForeignKey(POST, on_delete=models.CASCADE, related_name="post_likes")

    def __str__(self):
        return f"{self.user} liked {self.post.slug}"




