from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Auction, Comment, Bet, WatchList
from .forms import AuctionForm, CommentForm, BetForm, NewBetForm, WatchListForm


def index(request):

    return render(request, "auctions/index.html", {
    "auctions": reversed(Auction.objects.all())
    })

def my(request):

    return render(request, "auctions/my.html", {
    "auctions": reversed(Auction.objects.all())
    })

def page(request, pk, status):
    #extract data from the database
    current_auction = Auction.objects.get(id=pk)
    if request.user.username:
        current_user = User.objects.get(username=request.user.username)

    try:
        watched = WatchList.objects.get(watcher=current_user, page=current_auction)
    except:
        watched = ''

    current_bet = Bet.objects.get(id=pk)
    comments = Comment.objects.filter(source=current_auction)


    #create forms
    com_form = CommentForm()
    bet_form = NewBetForm()

    if watched:
        watch_form = WatchListForm(initial={
            'follow': watched.follow
            })
    else:
        watch_form = WatchListForm()

    if status == 'active':
        if request.method == "POST":
            new_com_form = CommentForm(request.POST)
            new_bet_form = NewBetForm(request.POST)
            new_watch_form = WatchListForm(request.POST)

            if new_com_form.is_valid():
                comment = new_com_form.cleaned_data["comment"]
                new_comment = Comment(comment=comment, source=current_auction,
                    com_author=current_user)
                new_comment.save()

            elif new_bet_form.is_valid():
                new_bet = new_bet_form.cleaned_data["current_bet"]

                if new_bet <= current_bet.current_bet:
                    return render(request, "auctions/page.html", {
                        "auction": current_auction,
                        "comments": reversed(comments),
                        "bet": Bet.objects.get(id=pk),
                        "com_form": com_form,
                        "bet_form": bet_form,
                        "watch_form": watch_form,
                        "message": "Warning! The new bid must be higher than the previous one."
                    })
                else:
                    Bet.objects.filter(id=pk).update(current_bet=new_bet,
                        bet_author=current_user)

            elif new_watch_form.is_valid():
                like = new_watch_form.cleaned_data["follow"]
                if watched:
                    like = new_watch_form.cleaned_data["follow"]
                    WatchList.objects.filter(watcher=current_user, page=current_auction).update(follow=like)
                else:
                    new_follow = WatchList(watcher=current_user, page=current_auction, follow=like)
                    new_follow.save()

            return HttpResponseRedirect(reverse("page", args=(pk, status,)))

        else:
            return render(request, "auctions/page.html", {
                "auction": current_auction,
                "comments": reversed(comments),
                "bet": current_bet,
                "com_form": com_form,
                "bet_form": bet_form,
                "watch_form": watch_form
            })
    else:
        if current_auction.status == 'active':
            Auction.objects.filter(id=pk).update(status=status)
        else:
            return render(request, "auctions/page.html", {
                "auction": current_auction,
                "comments": reversed(comments),
                "bet": current_bet,
                "com_form": com_form,
                "bet_form": bet_form,
                "watch_form": watch_form
            })

        return HttpResponseRedirect(reverse("page", args=(pk, status,)))

def categories(request):
    uniq_categories = []
    auctions = Auction.objects.all()

    return render(request, "auctions/categories.html", {
        "categories": uniq_categories,
        "auctions": reversed(Auction.objects.all())
    })

def sel_cat(request, cat):

    return render(request, "auctions/category.html", {
    "auctions": reversed(Auction.objects.filter(categorie=cat)),
    "category": cat
    })

def watchlist(request):
    watcher = User.objects.get(username=request.user.username)
    watches = WatchList.objects.filter(watcher=watcher, follow='True')
    return render(request, "auctions/watchlist.html", {
    "auctions": reversed(Auction.objects.all()),
    "watches": reversed(watches)
    })

def wonauctions(request):
    return render(request, "auctions/wonauctions.html", {
    "auctions": reversed(Auction.objects.all())
    })

def create(request):
    if request.method == "POST":
        auc_form = AuctionForm(request.POST, request.FILES)
        bet_form = BetForm(request.POST)
        if auc_form.is_valid() and bet_form.is_valid():
            name = auc_form.cleaned_data["name"]
            categorie = auc_form.cleaned_data["categorie"]
            description = auc_form.cleaned_data["description"]
            photo = auc_form.cleaned_data["photo"]
            current_bet = bet_form.cleaned_data["current_bet"]
            pub_author = User.objects.get(username=request.user.username)
            try:
                bet = Bet(current_bet=current_bet, bet_author=pub_author)
                bet.save()
                auction = Auction(name=name, categorie=categorie,
                    description=description, photo=photo, price=bet,
                    pub_author=pub_author)
                auction.save()

            except IntegrityError:
                return render(request, "auctions/create.html", {
                    "message": "Error! Try again. All forms must be full."
                })
            return HttpResponseRedirect(reverse("index"))
    else:
        auc_form = AuctionForm()
        bet_form = BetForm()
        return render(request, "auctions/create.html", {
        "auc_form": auc_form,
        "bet_form": bet_form
        })


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
