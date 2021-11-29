from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("listings/<int:listing_id>", views.listing, name="listing"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.category, name="category"),
    path("categories/<int:category_id>", views.one_category, name="one_category"),
    path("create", views.create_listing, name="create"),
    path("closed", views.closed, name="closed"),
    path("update/<int:listing_id>", views.update_listing, name="update"),
    path("delete/<int:listing_id>", views.delete_listing, name="delete"),
    path("listings/<int:listing_id>/add_bid", views.add_bid, name="add_bid"),
    path("listings/<int:listing_id>/close_bid", views.close_bid, name="close_bid"),
    path("listings/<int:listing_id>/add_comment", views.add_comment, name="add_comment"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("listings/<int:listing_id>/add_watchlist", views.add_watchlist, name="add_watchlist"),
    path("listings/<int:listing_id>/remove_watchlist", views.remove_watchlist, name="remove_watchlist")
]
