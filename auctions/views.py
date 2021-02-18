from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Bid, Listing, Comment, Watchlist, Closedbid, Alllisting
from datetime import datetime
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404


def register(request):
    item_listing = Listing.objects.all()
    items_count = len(item_listing)

    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match.",
                "items_count": items_count
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken.",
                "items_count": items_count
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html", {
            "items_count": items_count
        })


def login_view(request):
    item_listing = Listing.objects.all()
    items_count = len(item_listing)

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
                "message": "Invalid username and/or password.",
                "items_count": items_count
            })

    else:
        return render(request, "auctions/login.html", {
            "items_count": items_count
        })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def index(request):
    try:
        items = Listing.objects.order_by('-id')  # from newest to oldest
        items_count = len(items)
        watchlist = Watchlist.objects.filter(user=request.user.username)
        watchlist_count = len(watchlist)
        item_won = Closedbid.objects.filter(winner=request.user.username)
        items_won_count = len(item_won)
    except:
        items_count = None
        watchlist_count = None
    return render(request, "auctions/index.html", {
        "items": items,
        "items_count": items_count,
        "watchlist_count": watchlist_count,
        "items_won_count": items_won_count
    })


@login_required
def categories(request):
    try:
        item_listing = Listing.objects.all()
        items_count = len(item_listing)
        watchlist = Watchlist.objects.filter(user=request.user.username)
        watchlist_count = len(watchlist)
        item_won = Closedbid.objects.filter(winner=request.user.username)
        items_won_count = len(item_won)
        # RawQuerySet
        items = Listing.objects.raw(
            "SELECT * FROM auctions_listing GROUP BY category")
    except:
        items_count = None
        watchlist_count = None
    return render(request, "auctions/categories.html", {
        "items_count": items_count,
        "watchlist_count": watchlist_count,
        "items_won_count": items_won_count,
        "items": items
    })


@login_required
def category(request, category):
    try:
        item_listing = Listing.objects.all()
        items_count = len(item_listing)
        watchlist = Watchlist.objects.filter(user=request.user.username)
        watchlist_count = len(watchlist)
        items_category = Listing.objects.filter(category=category)
        item_won = Closedbid.objects.filter(winner=request.user.username)
        items_won_count = len(item_won)
    except:
        items_count = None
        watchlist_count = None
    return render(request, "auctions/category.html", {
        "items_count": items_count,
        "watchlist_count": watchlist_count,
        "items_won_count": items_won_count,
        "items": items_category,
        "category": category,
    })


@login_required
def create(request):
    try:
        item_listing = Listing.objects.all()
        items_count = len(item_listing)
        watchlist = Watchlist.objects.filter(user=request.user.username)
        watchlist_count = len(watchlist)
        item_won = Closedbid.objects.filter(winner=request.user.username)
        items_won_count = len(item_won)
    except:
        items_count = None
        watchlist_count = None
    return render(request, "auctions/create.html", {
        "items_count": items_count,
        "watchlist_count": watchlist_count,
        "items_won_count": items_won_count
    })


@login_required
def create_submit(request):
    if request.method == "POST":
        list = Listing()
        now = datetime.now()
        date_time = now.strftime(
            "%d.%m.%Y, %H:%M:%S")  # The strftime() method returns a string representing date and time using date, time or datetime object.
        list.owner = request.user.username
        list.title = request.POST.get('title')
        list.description = request.POST.get('description')
        list.category = request.POST.get('category')
        list.price = request.POST.get('price')
        list.url = request.POST.get('url')
        list.time = date_time  # Dete 20.09.2020, 06:51:31
        list.save()

        all_list = Alllisting()
        items = Listing.objects.all()
        for i in items:
            try:
                if Alllisting.objects.get(listingid=i.id):
                    pass
            except:
                all_list.listingid = i.id
                all_list.title = i.title
                all_list.description = i.description
                all_list.url = i.url
                all_list.save()
        messages.success(request, 'New Listing has been created successfully.')
        return redirect('index')
    else:
        return redirect('index')


def details(request, id):
    try:
        item = get_object_or_404(Listing, id=id)
    except:
        return redirect('index')

    try:
        comments = Comment.objects.filter(listingid=id)
    except:
        comments = None

    if request.user.username:

        try:
            if get_object_or_404(Watchlist, user=request.user.username, listingid=id):
                added = True
        except:
            added = False

        try:
            list_detail = get_object_or_404(Listing, id=id)
            if list_detail.owner == request.user.username:
                owner = True
            else:
                owner = False
        except:
            return redirect('index')

    else:
        added = False
        owner = False

    try:
        item_listing = Listing.objects.all()
        items_count = len(item_listing)
        watchlist = Watchlist.objects.filter(user=request.user.username)
        watchlist_count = len(watchlist)
        item_won = Closedbid.objects.filter(winner=request.user.username)
        items_won_count = len(item_won)
    except:
        items_count = None
        watchlist_count = None
    return render(request, "auctions/details.html", {
        "items_count": items_count,
        "watchlist_count": watchlist_count,
        "items_won_count": items_won_count,
        "item": item,
        "error": request.COOKIES.get('error'),
        "success": request.COOKIES.get('success'),
        "comments": comments,
        "added": added,
        "owner": owner,
    })


@login_required
def bid_submit(request, listingid):
    current_bid = get_object_or_404(Listing, id=listingid)
    current_bid = current_bid.price

    if request.method == "POST":
        user_bid = int(request.POST.get("bid"))

        # Max bid is $9 9999.00
        if (user_bid > current_bid) and (user_bid < 10000):
            listing_items = get_object_or_404(Listing, id=listingid)
            listing_items.price = user_bid
            listing_items.save()

            try:
                if Bid.objects.filter(id=listingid):
                    offer = Bid.objects.filter(id=listingid)
                    offer.delete()
                rates = Bid()
                rates.user = request.user.username
                rates.title = listing_items.title
                rates.listingid = listingid
                rates.bid = user_bid
                rates.save()
            except:
                rates = Bid()
                rates.user = request.user.username
                rates.title = listing_items.title
                rates.listingid = listingid
                rates.bid = user_bid
                rates.save()
            response = redirect('details', id=listingid)
            response.set_cookie('success', 'Bid successful!', max_age=1)
            return response
        else:
            response = redirect('details', id=listingid)
            response.set_cookie('error', 'Bid too low!', max_age=1)
            return response
    else:
        return redirect('index', )


@login_required
def comment_submit(request, listingid):
    if request.method == "POST":
        now = datetime.now()
        date_time = now.strftime(
            "%d.%m.%Y, %H:%M:%S")  # The strftime() method returns a string representing date and time using date, time or datetime object.
        c = Comment()
        c.comment = request.POST.get('comment')
        c.user = request.user.username
        c.time = date_time
        c.listingid = listingid
        c.save()
        return redirect('details', id=listingid)
    else:
        return redirect('index')


@login_required
def show_watchlist(request, username):
    if request.user.username:
        try:
            watchlist = Watchlist.objects.filter(user=username)
            items = []
            for i in watchlist:
                items.append(Listing.objects.filter(id=i.listingid))
            try:
                watchlist = Watchlist.objects.filter(user=request.user.username)
                watchlist_count = len(watchlist)
                item_listing = Listing.objects.all()
                items_count = len(item_listing)
                item_won = Closedbid.objects.filter(winner=request.user.username)
                items_won_count = len(item_won)
            except:
                watchlist_count = None
                items_count = None
            return render(request, "auctions/show_watchlist.html", {
                "items": items,
                "items_count": items_count,
                "watchlist_count": watchlist_count,
                "items_won_count": items_won_count
            })
        except:
            try:
                watchlist = Watchlist.objects.filter(user=request.user.username)
                watchlist_count = len(watchlist)
                item_listing = Listing.objects.all()
                items_count = len(item_listing)
                item_won = Closedbid.objects.filter(winner=request.user.username)
                items_won_count = len(item_won)
            except:
                watchlist_count = None
                items_count = None
            return render(request, "auctions/show_watchlist.html", {
                "items": None,
                "items_count": items_count,
                "watchlist_count": watchlist_count,
                "items_won_count": items_won_count
            })
    else:
        return redirect('index')


@login_required
def add_watchlist(request, listingid):
    if request.user.username:
        watchlist = Watchlist()
        watchlist.user = request.user.username
        watchlist.listingid = listingid
        watchlist.save()
        messages.success(request, 'Added to Watchlist successfully.')
        return redirect('details', id=listingid)
    else:
        return redirect('index')


@login_required
def remove_watchlist(request, listingid):
    if request.user.username:
        try:
            watchlist = get_object_or_404(Watchlist, user=request.user.username, listingid=listingid)
            watchlist.delete()
            messages.success(request, 'Removed from Watchlist successfully.')
            return redirect('details', id=listingid)
        except:
            return redirect('details', id=listingid)
    else:
        return redirect('index')


@login_required
def close_bid(request, listingid):
    if request.user.username:
        try:
            listing = get_object_or_404(Listing, id=listingid)
        except:
            return redirect('index')
        close_bid = Closedbid()
        title = listing.title
        close_bid.owner = listing.owner
        close_bid.listingid = listingid

        try:
            offer = get_object_or_404(Bid, listingid=listingid, bid=listing.price)
            close_bid.winner = offer.user
            close_bid.winprice = offer.bid
            close_bid.save()
            offer.delete()
        except:
            close_bid.winner = listing.owner
            close_bid.winprice = listing.price
            close_bid.save()

        if Watchlist.objects.filter(listingid=listingid):
            watch = Watchlist.objects.filter(listingid=listingid)
            watch.delete()
        else:
            pass

        try:
            comm = Comment.objects.filter(listingid=listingid)
            comm.delete()
        except:
            pass

        try:
            brow = Bid.objects.filter(listingid=listingid)
            brow.delete()
        except:
            pass

        try:
            cb_list = get_object_or_404(Closedbid, listingid=listingid)
        except:
            close_bid.owner = listing.owner
            close_bid.winner = listing.owner
            close_bid.listingid = listingid
            close_bid.winprice = listing.price
            close_bid.save()
            cb_list = get_object_or_404(Closedbid, listingid=listingid)
        listing.delete()
        try:
            watchlist = Watchlist.objects.filter(user=request.user.username)
            watchlist_count = len(watchlist)
            item_listing = Listing.objects.all()
            items_count = len(item_listing)
            item_won = Closedbid.objects.filter(winner=request.user.username)
            items_won_count = len(item_won)
        except:
            watchlist_count = None
            items_count = None
        return render(request, "auctions/congratulations.html", {
            "items_count": items_count,
            "watchlist_count": watchlist_count,
            "items_won_count": items_won_count,
            "close_bid": cb_list,
            "title": title
        })
    else:
        return redirect('index')


@login_required
def won(request):
    if request.user.username:
        items = []
        try:
            wons = Closedbid.objects.filter(winner=request.user.username)
            for w in wons:
                items.append(Alllisting.objects.filter(listingid=w.listingid))
        except:
            items = None
            wons = None
        try:
            watchlist = Watchlist.objects.filter(user=request.user.username)
            watchlist_count = len(watchlist)
            item_listing = Listing.objects.all()
            items_count = len(item_listing)
            item_won = Closedbid.objects.filter(winner=request.user.username)
            items_won_count = len(item_won)
        except:
            watchlist_count = None
            items_count = None
        return render(request, 'auctions/won.html', {
            "items": items,
            "items_count": items_count,
            "watchlist_count": watchlist_count,
            "items_won_count": items_won_count,
            "wons": wons
        })
    else:
        return redirect('index')
