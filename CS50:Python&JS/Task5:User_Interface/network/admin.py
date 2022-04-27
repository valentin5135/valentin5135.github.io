from django.contrib import admin

from .models import User, Follower, Comment, Post, Like

# Register your models here.
admin.site.register(User)
admin.site.register(Follower)
admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(Like)
