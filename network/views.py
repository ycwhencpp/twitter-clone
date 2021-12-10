import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User,make_tweet,tweet_comment
from .forms import tweetform,commentform

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


def index(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            tweet=tweetform(request.POST)
            if tweet.is_valid():
                tweet.instance.author=request.user
                tweet.save()
            return HttpResponseRedirect(reverse("index"))

    tweets=make_tweet.objects.all()
    return render(request, "network/index.html",{
        "tweets":tweets,
        "tweet_form":tweetform,
    })


            
@login_required
@csrf_exempt
def editpost(request):
    if request.method == "PUT":
        data=json.loads(request.body)

        try:
            tweet=make_tweet.objects.get(id=id)
        except make_tweet.DoesNotExist:
            return JsonResponse({"error":"Tweet not found"},status=404)
        content=data.get("content","")
        like=data.get("liked","")
        rt=data.get("retweet","")

        if content:
            
            if request.user == tweet.author :
                
                tweet.content=content
            else:
                return JsonResponse({"error":"can edit your post only"},status=400)
        
        if like:
            
            if request.user in tweet.liked.all():
                tweet.liked.remove(request.user)
            else:
                tweet.liked.add(request.user)
        if rt:
            
            if request.user in tweet.retweet.all():
                tweet.retweet.remove(request.user)
            else:
                tweet.retweet.add(request.user)
        tweet.save()
        return JsonResponse({"message":"post updated successfully","likes_count":str(tweet.likecount()),"retweetcount":str(tweet.retweetcount())},status=201)
    
    return JsonResponse({"error":"Only PUT request is Valid"},status=400)

def view_profile(request,username):
    viewed_profile=User.objects.get(username=username)
    return render(request,"network/profile.html",{
        "profile":viewed_profile,
    })

@login_required
@csrf_exempt
def editprofile(request):
    if request.method =="PUT":
        data=json.loads(request.body)
        username=data.get("username")
        try:
            viewed_user=User.objects.get(username=username)
            current_user=User.objects.get(username=request.user)
        except:
            return JsonResponse({"error":"Cant find user details"},status=404)
        if data["following"]:
            if current_user == viewed_user:
                return JsonResponse({"error":"cant follow yourself"},status=400)
            if viewed_user in current_user.is_following.all():
                print("followed")
                viewed_user.followers.remove(current_user)
            else:
                print("non followed")
                viewed_user.followers.add(current_user)

        return JsonResponse({"message":"Followed or Unfollowed Succesfully","followerscount":viewed_user.followers.all().count(),"followingcount":viewed_user.is_following.all().count()})
    return JsonResponse({"error":"only Put request is valid"},status=400)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
