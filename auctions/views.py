from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages

from .models import User, Listing, Category, Comment, Bid
from .forms import ListingCreateForm

def index(request):
    listings = Listing.objects.filter(is_active=True)
    data = {
        "listings": listings,    
    }
    return render(request, "auctions/index.html", data)

def closed(request):
    listings = Listing.objects.filter(is_active=False)
    data = {
        "listings": listings,     
    }
    return render(request, "auctions/closed.html", data)

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


def listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    comments = Comment.objects.all()
    bids = Bid.objects.all()
    user = request.user
    data = {
		"listing": listing,
        "comments": comments,
        "bids": bids,
	}
    return render(request, 'auctions/listing.html', data)


@login_required
def create_listing(request):
    form = ListingCreateForm()
    
    if request.method == 'POST':
        form = ListingCreateForm(request.POST)

        if form.is_valid():
            new_listing = Listing.objects.create(
                author = request.user,
                title = form.cleaned_data["title"],
                description = form.cleaned_data["description"],
                starting_bid = form.cleaned_data["starting_bid"],
                category = form.cleaned_data["category"],
                img_url = form.cleaned_data["img_url"],
                date = form.cleaned_data["date"],
            )
            new_listing.save()
            messages.add_message(request, messages.SUCCESS, "Your listing is Successfully created")
            return redirect('/')

    data ={'form': form}
    return render(request, "auctions/create.html", data)

@login_required
def update_listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    form = ListingCreateForm(instance=listing)

    if request.method == 'POST':
        form = ListingCreateForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('/')

    data = {
        'form': form
        }
    return render(request, "auctions/create.html", data)

@login_required
def delete_listing(request, listing_id):
    listing= Listing.objects.get(id=listing_id)
    if request.method == 'POST':      
        listing.delete()
        return redirect('/')

    data = {
        'listing': listing
        }
    return render(request, "auctions/delete.html", data)

@login_required
def close_bid(request, listing_id):
    user = request.user
    listing= Listing.objects.get(id=listing_id)
    if user == listing.author:
        listing.is_active = False      
        listing.save()
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
    else:
        listings = Listing.objects.filter(is_active=True)
        data = {
            'listings': listings 
            }
        return render(request, "auctions/index.html", data)

@login_required
def watchlist(request):
    user = request.user
    listing = user.watchlist.filter(is_active=True) 
    data = { 
        'listing': listing,
        }
    return render(request, "auctions/watchlist.html", data)

@login_required
def add_watchlist(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    user = request.user
    listing.watcher.add(user)
    listing.save()
    messages.add_message(request, messages.SUCCESS, "Successfully added to your watchlist")
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

@login_required
def remove_watchlist(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    user = request.user
    listing.watcher.remove(user)
    listing.save()
    messages.add_message(request, messages.SUCCESS, "Successfully removed from your watchlist")
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

@login_required
def add_bid(request, listing_id):
    if request.method == 'POST':
        listing = Listing.objects.get(id=listing_id)
        bidder = request.user
        new_bid = float(request.POST.get('bid'))
        bid = Bid.objects.create(listing=listing, new_bid=new_bid, bidder=bidder)
        if new_bid > listing.starting_bid:
            if listing.current_bid is None:
                listing.current_bid = new_bid
                listing.buyer = bidder
                bid.user = bidder
                bid.listing = listing
                bid.save()
                listing.save()
                messages.add_message(request, messages.SUCCESS, "Your bid Successfully added")
                return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
            elif new_bid > listing.current_bid:
                listing.current_bid = new_bid
                listing.buyer = bidder
                bid.user = bidder
                bid.listing = listing
                bid.save()
                listing.save()
                messages.add_message(request, messages.SUCCESS, "Your bid Successfully added")
                return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
            elif new_bid == listing.current_bid or new_bid == listing.starting_bid:
                messages.add_message(request, messages.ERROR, "Your bid should be higher than previous one")
                return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
        else:
            messages.add_message(request, messages.ERROR, "Your bid should be higher than previous one")
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

@login_required
def add_comment(request, listing_id):
    if request.method == 'POST':
        listing = Listing.objects.get(id=listing_id)
        comment_text = request.POST['comment']
        comment = Comment.objects.create(listing=listing, comment=comment_text, commenter=request.user)
        comment.save()
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

def category(request):
	categories = Category.objects.all()
	data = {
		"categories": categories,
	}
	return render(request, 'auctions/categories.html', data)

def one_category(request, category_id):
	categories = Category.objects.all()
	listing = Listing.objects.filter(is_active=True)
	if category_id:
		category = get_object_or_404(Category, pk=category_id)
		listing = listing.filter(category=category)
		data = {
			'categories': categories,
			'category': category,
			'listing': listing
		}
	return render(request, 'auctions/one_category.html', data)