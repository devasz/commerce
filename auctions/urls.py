from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("category/<str:category>", views.category, name="category"),
    path("create", views.create, name="create"),
    path("create_submit",views.create_submit,name="create_submit"),
    path("details/<int:id>",views.details,name="details"),
    path("bid_submit/<int:listingid>",views.bid_submit,name="bid_submit"),
    path("comment_submit/<int:listingid>",views.comment_submit,name="comment_submit"),
    path("add_watchlist/<int:listingid>",views.add_watchlist,name="add_watchlist"),
    path("remove_watchlist/<int:listingid>",views.remove_watchlist,name="remove_watchlist"),
    path("show_watchlist/<str:username>", views.show_watchlist, name="show_watchlist"),
    path("close_bid/<int:listingid>",views.close_bid,name="close_bid"),
    path("won",views.won,name="won")
]
