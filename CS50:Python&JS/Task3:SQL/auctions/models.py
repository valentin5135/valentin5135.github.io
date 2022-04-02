from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    def __str__(self):
        return f"{self.username}"

class Bet(models.Model):
    current_bet = models.FloatField()
    bet_author = models.ForeignKey(User, on_delete=models.CASCADE,
        related_name="shoper")

    def __str__(self):
        return f"{self.current_bet}"

class Auction(models.Model):
    name = models.CharField(max_length=128)
    categorie = models.CharField(max_length=64)
    description = models.TextField()
    photo = models.ImageField(max_length=1024,
        upload_to="photos", default="photos/no_photo.png")
    price = models.ForeignKey(Bet, on_delete=models.CASCADE,
        related_name="last_bet")
    status = models.CharField(max_length=16, default="active")
    pub_author = models.ForeignKey(User, on_delete=models.CASCADE,
        related_name="creator")
    pub_data = models.DateTimeField(auto_now=True)

    @property
    def photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url

    def __str__(self):
        return f"{self.name} by {self.pub_author}"

class Comment(models.Model):
    com_author = models.ForeignKey(User, on_delete=models.CASCADE,
        related_name="commentor")
    source = models.ForeignKey(Auction, on_delete=models.CASCADE,
        related_name="publicated")
    comment = models.TextField()
    com_data = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}: from {self.com_author} to {self.source}"

class WatchList(models.Model):
    watcher = models.ForeignKey(User, on_delete=models.CASCADE,
        related_name="follower")
    page = models.ForeignKey(Auction, on_delete=models.CASCADE,
        related_name="source")
    follow = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.follow}"
