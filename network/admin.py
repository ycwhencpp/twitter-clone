from django.contrib import admin
from .models import make_tweet, mutuals, tweet_comment,User
# Register your models here.

admin.site.register(make_tweet)
admin.site.register(tweet_comment)
admin.site.register(User)
admin.site.register(mutuals)