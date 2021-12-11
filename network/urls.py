
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>", views.view_profile, name="view_profile"),
    path("following", views.following, name="following"),
    path("comment/<int:id>", views.comment, name="comment"),
    path("tweet/<int:id>", views.view_tweet, name="view_tweet"),
    
    # API ROUTES
    path("editpost", views.editpost, name="editpost"),
    path("editprofile", views.editprofile, name="editprofile")


]
