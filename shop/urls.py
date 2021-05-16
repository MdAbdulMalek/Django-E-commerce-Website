from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("home/", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contract/", views.contract, name="contract"),
    path("tracker/", views.tracker, name="tracker"),
    path("search/", views.search, name="search"),
    path("productview/<int:myid>", views.productview, name="productview"),
    path("checkout/", views.checkout, name="checkout"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout, name="logout"),
    path("allprod/<str:category>", views.allprod, name="allprod")
]