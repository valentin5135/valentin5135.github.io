import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from operator import attrgetter
from django.core.paginator import Paginator

from .models import User, Follower, Post, Comment, Like


def index(request):
    posts = Post.objects.order_by("-post_date").all()
    paginator = Paginator(posts, 10) # Show 10 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "YouControl/index.html", {
        "posts": posts,
        "page_obj": page_obj
    })
def create(request):

        return render(request, "YouControl/create.html")

def create_post(request):

    # Composing a new email must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Get contents of email
    data = json.loads(request.body)
    post_name = data.get("post_name")
    description = data.get("description")
    tin = data.get("tin")
    sert_num = data.get("sert_num")
    author = User.objects.get(username=request.user)
    post = Post(post_author=author, post_name=post_name, description=description,
        tin=tin, sert_num=sert_num)
    post.save()

    #return HttpResponseRedirect(reverse("index"))
    return JsonResponse({"message": "Creating post successfully."}, status=201)

def following(request):
    posts = []
    followings = Follower.objects.filter(follower=request.user)
    for follow in followings:
        posts_block = Post.objects.filter(post_author=follow.following)
        for post in posts_block:
            posts.append(post)

    sorted_posts = list(reversed(sorted(posts, key=attrgetter('post_date'))))

    paginator = Paginator(sorted_posts, 10) # Show 10 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "YouControl/following.html", {
        "posts": sorted_posts,
        "page_obj": page_obj
    })

def profile(request, pk):

    author = User.objects.get(pk=pk)
    posts = Post.objects.filter(post_author=author).order_by("-post_date")

    try:
        subscribed = Follower.objects.get(follower=request.user, following=author)
    except Follower.DoesNotExist:
        subscribed = None;

    paginator = Paginator(posts, 10) # Show 10 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "YouControl/profile.html", {
        "author": author,
        "followers": Follower.objects.filter(following=author).count(),
        "followings": Follower.objects.filter(follower=author).count(),
        "posts": posts,
        "posts_count": posts.count(),
        "subscribed":  subscribed,
        "page_obj": page_obj
    })

def post(request, post_id):

    # Query for requested post
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # Return email contents
    if request.method == "GET":
        return JsonResponse(post.serialize())

    # Update whether post is likes
    elif request.method == "PUT":
        data = json.loads(request.body)

        if data.get("post_name") or data.get("description") or data.get("tin") or data.get("sert_num") or data.get("sert_status") is not None:
            new_post = Post.objects.filter(pk=post_id).update(post_name=data.get("post_name"), description=data.get("description"), tin=data.get("tin"),
                sert_num=data.get("sert_num"), sert_status=data.get("sert_status"))
            return HttpResponse(new_post)
        else:
            return HttpResponse({"error": "Post can't be empty."}, status=404)

    # Post must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)

def follow(request, profile_id):

    try:
        profile = User.objects.get(id=profile_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)


    # Query for requested post
    try:
        follows = Follower.objects.filter(following=profile)
    except Follower.DoesNotExist:
        return JsonResponse({"error": "Follow not found."}, status=404)

    # Return email contents
    if request.method == "GET":
        return JsonResponse([follow.serialize() for follow in follows], safe=False)

    # Update whether post is likes
    elif request.method == "PUT":
        data = json.loads(request.body)

        try:
            check = Follower.objects.get(following=profile, follower=request.user)
        except Follower.DoesNotExist:
            check = ''

        if not check:
            new_follow = Follower(following=profile, follower=request.user)
            new_follow.save()

        if check:
            check.delete()

        try:
            result = Follower.objects.get(
                following=profile, follower=request.user)
        except Follower.DoesNotExist:
            result = ''

        return HttpResponse(result)
    # Post must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)

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
            return render(request, "YouControl/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "YouControl/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        fullname = request.POST["fullname"]
        email = request.POST["email"]
        tel_number = request.POST["tel_number"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "YouControl/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, fullname=fullname, email=email, tel_number=tel_number, password=password)
            user.save()
        except IntegrityError:
            return render(request, "YouControl/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "YouControl/register.html")
