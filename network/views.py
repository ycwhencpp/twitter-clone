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

from django.core.paginator import Paginator

def index(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            tweet=tweetform(request.POST)
            if tweet.is_valid():
                tweet.instance.author=request.user
                tweet.save()
            return HttpResponseRedirect(reverse("index"))

    tweets=make_tweet.objects.all()
    paginator=Paginator(tweets,10)
    page_number=request.GET.get("page")
    page_obj=paginator.get_page(page_number)
    return render(request, "network/index.html",{
        "page_obj":page_obj,
        "tweet_form":tweetform,
        
    })


            
@login_required
@csrf_exempt
def editpost(request):
    if request.method == "PUT":

        # getting id from the request body
        data=json.loads(request.body)
        id=data.get("id")

        # querying db for the tweet related to that id 
        try:
            tweet=make_tweet.objects.get(id=id)
        except make_tweet.DoesNotExist:
            return JsonResponse({"error":"Tweet not found"},status=404)

        # storing data from the request to some variables
        content=data.get("content","")
        like=data.get("liked","")
        rt=data.get("retweet","")

        # if request contains content 
        if content:

            # changing content of tweet to new content entered if user is the author of that tweet
            if request.user == tweet.author :
                tweet.content=content
            else:
                return JsonResponse({"error":"can edit your post only"},status=400)
        
        # if request contains like = true or user clicked on like button
        if like:
            
            # if user has already liked that post then unliking it otherwise liking it 
            if request.user in tweet.liked.all():
                tweet.liked.remove(request.user)
            else:
                tweet.liked.add(request.user)

        # if request contains retweet = true or user clicked on retweet button
        if rt:

            # if user has already retweeted that post then undo it otherwise retweet it 
            if request.user in tweet.retweet.all():
                tweet.retweet.remove(request.user)
            else:
                tweet.retweet.add(request.user)

        # saving all changes made to that tweet and then returing likes and rt count in json format so that
        # we can update  html instantly with help of js
        tweet.save()
        return JsonResponse({"message":"post updated successfully","likes_count":str(tweet.likecount()),"retweetcount":str(tweet.retweetcount())},status=201)
    
    return JsonResponse({"error":"Only PUT request is Valid"},status=400)




def view_profile(request,username):

    # getting viewed_user profile and its following info
    viewed_profile=User.objects.get(username=username)
    viewed_profile_following=viewed_profile.is_following.all()

    # looping over all followers and getting their tweets
    for users in viewed_profile_following:
        tweet=users.tweet.all()
    # pagination
    paginate=Paginator(tweet,10)
    page_number=request.GET.get("page")
    page_obj=paginate.get_page(page_number)
    return render(request,"network/profile.html",{
        "profile":viewed_profile,
        "page_obj":page_obj,
    })



@login_required
@csrf_exempt
def editprofile(request):
    if request.method =="PUT":

        # getting username from the request data
        data=json.loads(request.body)
        username=data.get("username")

        # querying db for the current user and viewed user
        try:
            viewed_user=User.objects.get(username=username)
            current_user=User.objects.get(username=request.user)
        except:
            return JsonResponse({"error":"Cant find user details"},status=404)

        # if the request contains following =  true or user has clicked on follow button 
        if data["following"]:

            # if currents user is not same as viewed user i.e; you are not trying to follow yourself
            if current_user != viewed_user:

                # if viewed user is already in current user following then removing it otherwise adding him 
                if viewed_user in current_user.is_following.all():
                    print("followed")
                    viewed_user.followers.remove(current_user)
                else:
                    print("not followed")
                    viewed_user.followers.add(current_user)
            else:
                return JsonResponse({"error":"cant follow yourself"},status=400)

        # sending followers count and following count so that we can update html instantly with the help of js 
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
