from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

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
    post_content = models.TextField()
    post_date = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(default=0)

    def serialize(self):
        return {
            "id": self.id,
            "author": self.post_author.username,
            "content": self.post_content,
            "date": self.post_date,
            "likes": self.likes
        }

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
