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

    return render(request, "network/index.html", {
        "posts": posts,
        "page_obj": page_obj
    })

def create_post(request):

    # Composing a new email must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Get contents of email
    data = json.loads(request.body)
    content = data.get("content")
    author = User.objects.get(username=request.user)
    post = Post(post_author=author, post_content=content)
    post.save()

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

    return render(request, "network/following.html", {
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

    return render(request, "network/profile.html", {
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

        if data.get("content") is not None:
            new_post = Post.objects.filter(pk=post_id).update(post_content=data.get("content"))
            return HttpResponse(new_post)
        else:
            return HttpResponse({"error": "Post can't be empty."}, status=404)

    # Post must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)

def like(request, post_id):

    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # Query for requested post
    try:
        likes = Like.objects.filter(source=post)
    except Like.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # Return email contents
    if request.method == "GET":
        return JsonResponse([like.serialize() for like in likes], safe=False)

    # Update whether post is likes
    elif request.method == "PUT":
        data = json.loads(request.body)

        try:
            user = User.objects.get(username=data["liker"])
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found."}, status=404)


        try:
            check = Like.objects.get(liker=user, source=post)
        except Like.DoesNotExist:
            check = ''

        if check:
            check.delete()
        elif not check:
            new_like = Like(liker=user, source=post)
            new_like.save()

        likes = Like.objects.filter(source=post).count()
        Post.objects.filter(id=post_id).update(likes=likes)
        return HttpResponse(likes)

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
