from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path("",views.StartingPageView.as_view(),name="starting-page"),
    path("posts",views.AllPostView.as_view(),name="posts-page"),
    path("posts/<slug:slug>",views.SinglePostView.as_view(),name="post-detail-page"),
    path("about-me",views.about,name="about-me"),
    path("books",views.books,name="books"),
    path("cart/",views.cart,name="cart"),
    path("cart/remove/",views.removefromcart,name="remove"),
    path("cart/checkout/",views.checkout,name="checkout"),
    path("cart/checkout/complete/",views.completeOrder,name="complete_order"),
    path("cart/checkout/complete/request", views.send_request, name='request'),
    path("verify/", views.verify , name='verify'),
    path("movies",views.movies,name="movies"),
    path("contact-us",views.contact,name="contact-us"),
]
