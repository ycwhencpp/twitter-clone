from .models import make_tweet,tweet_comment
from django import forms

class tweetform(forms.ModelForm):

    class Meta:
        model=make_tweet
        fields=['content']

        widgets={
            "content":forms.Textarea(attrs={"class":"form-control content","id":"tweet-content","placeholder":"What's In Your Mind ?","autocomplete":"off","autofocus":"off","rows":5}),
            # "img":forms.FileInput(attrs={"class":"form-control tweet-img","id":"formFile"})
        }
        labels={
            "content":""
        }

class commentform (forms.ModelForm):
    class Meta:
        model=tweet_comment
        fields=['comment']

        widgets={
            "comment":forms.Textarea(attrs={"class":"form-control content","placeholder":"Your View!","autocomplete":"off","rows":2}),
        }

