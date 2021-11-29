from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category_name = models.CharField(max_length=128, blank=True, null=True, default=None)

    def __str__(self):
        return str(self.category_name)

class Listing(models.Model):
    title = models.CharField(max_length=255, default=None)
    description = models.CharField(max_length=255, default=None)
    starting_bid = models.DecimalField(max_digits=6, decimal_places=2)
    current_bid = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, default=None)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, default=None)
    img_url = models.CharField(blank=True, max_length=255, default="https://image.shutterstock.com/image-vector/no-image-available-sign-internet-600w-261719003.jpg")
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="author")
    watcher = models.ManyToManyField(User, blank=True, related_name="watchlist")
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=None)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.title)

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids", default=None)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, default=None)
    new_bid = models.SmallIntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.bidder}'s bid for {self.listing}: {self.new_bid}$"

class Comment(models.Model):
    listing = models.ForeignKey(Listing, related_name="comments", on_delete=models.CASCADE)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, default=None)
    comment = models.TextField(default=None)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.commenter} {self.comment}"

