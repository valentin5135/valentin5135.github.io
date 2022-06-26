from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    fullname = models.CharField(max_length=128)
    tel_number = PhoneNumberField(unique = True, null = False, blank = False)

    def __str__(self):
        return f"{self.username}"

class Follower(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE,
        related_name="followings")
    follower = models.ForeignKey(User, on_delete=models.CASCADE,
        related_name="followers")

    def serialize(self):
        return {
            "id": self.id,
            "following": self.following.username,
            "follower": self.follower.username
        }

    def __str__(self):
        return f"{self.follower} follow for {self.following}"

class Post(models.Model):
    post_author = models.ForeignKey(User, on_delete=models.CASCADE,
        related_name="creator")
    post_name = models.CharField(max_length=128)
    description = models.TextField()
    tin = models.IntegerField()
    sert_num = models.IntegerField()
    sert_status = models.CharField(max_length=16, default="active")
    post_date = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(default=0)

    def serialize(self):
        return {
            "id": self.id,
            "author": self.post_author.username,
            "post_name": self.post_name,
            "description": self.description,
            "tin": self.tin,
            "sert_num": self.sert_num,
            "sert_status": self.sert_status,
            "date": self.post_date,
            "likes": self.likes
        }

    @property
    def photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url

    def __str__(self):
        return f"post #{self.id} by {self.post_author}"

class Like(models.Model):
    liker = models.ForeignKey(User, on_delete=models.CASCADE,
        related_name="like_author")
    source = models.ForeignKey(Post, on_delete=models.CASCADE,
        related_name="liked_post")

    def serialize(self):
        return {
            "id": self.id,
            "liker": self.liker.username,
            "source": self.source.id
        }

    def __str__(self):
        return f"{self.liker} likes {self.source}"


class Comment(models.Model):
    com_author = models.ForeignKey(User, on_delete=models.CASCADE,
        related_name="commentor")
    source = models.ForeignKey(Post, on_delete=models.CASCADE,
        related_name="publicated")
    comment = models.TextField()
    com_data = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"from {self.com_author} to {self.source}"
