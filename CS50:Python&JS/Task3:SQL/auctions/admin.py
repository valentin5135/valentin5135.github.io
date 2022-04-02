from django.contrib import admin
from .models import User, Auction, Comment, Bet, WatchList

# Register your models here.
admin.site.register(User)
admin.site.register(Auction)
admin.site.register(Comment)
admin.site.register(Bet)
admin.site.register(WatchList)
