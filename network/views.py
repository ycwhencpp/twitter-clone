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
# @login_required
# @csrf_exempt
# def create_tweet(request):
#     if request.method!="POST":
#         return JsonResponse({"Error":"POST request required."},status=400)
    
#     data=json.loads(request.body)
#     if data=={""}:
#         return JsonResponse({"error":"tweet can't be empty"},status=400)

#     content=data.get("content","")
#     tweet= make_tweet(
#         author=request.user,
#         content=content,
#     )
#     tweet.save()
#     return JsonResponse({"message": "tweet successfully Posted."}, status=201)

# @login_required
# @csrf_exempt
# def edit_post(request,pk):

#     try:
#         tweet=make_tweet.objects.get(user=request.user,id=pk)
#     except make_tweet.DoesNotExist:
#         return JsonResponse({"error":"Tweet not found"},status=404)
    
#     if request.method == "GET":
#         return JsonResponse(tweet.serialize())
    
#     elif request.method == "PUT":
#         data=json.loads(request.body)
#         if data.get("content") is not None:
#             tweet.content=data["content"]
#         if data.get("liked") is not None:
#             tweet.liked=data["liked"]
#         if data.get("retweet") is not None:
#             tweet.retweet=data["retweet"]
#         tweet.save()
#         return HttpResponse(status=204)

#     else:
#         return JsonResponse({"error":"GET or PUT request Required"},status=400)
            
@login_required
@csrf_exempt
def editpost(request):
    if request.method == "PUT":
        data=json.loads(request.body)
        print("data:",data)
        id=data.get("id","")
        print("id:",id)
        try:
            tweet=make_tweet.objects.get(id=id)
        except make_tweet.DoesNotExist:
            return JsonResponse({"error":"Tweet not found"},status=404)
        content=data.get("content","")
        like=data.get("liked","")
        rt=data.get("retweet","")
        print("content:",content)
        print("liked:",like)
        print("retweet:",rt)
        if content:
            print("1")
            if request.user == tweet.author :
                print("2")
                tweet.content=content
                print("3")
                print(tweet.content)
            else:
                return JsonResponse({"error":"can edit your post only"},status=400)
        print("-1")
        if like:
            print("4")
            if request.user in tweet.liked.all():
                tweet.liked.remove(request.user)
            else:
                tweet.liked.add(request.user)
        if rt:
            print("4")
            if request.user in tweet.retweet.all():
                tweet.retweet.remove(request.user)
            else:
                tweet.retweet.add(request.user)
        print("5")
        print(tweet)
        tweet.save()
        print("6")
        return JsonResponse({"message":"post updated successfully","likes_count":str(tweet.likecount())},status=201)
    
    return JsonResponse({"error":"Only PUT request is Valid"},status=400)






























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
