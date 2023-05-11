from django.urls import path

from . import views

urlpatterns = [
    path("home", views.index, name="index"),
    path("products", views.products, name="products"),
    path("products/<product_id>", views.showProduct, name="showProduct"),
    path('addFavourite/<product_id>', views.addFavourite, name='addFavourite'),
    path('addToCart/<product_id>', views.addToCart, name='addToCart'),
    path('deleteWishList', views.delWishList, name='deleteWishList'),
    path('deleteCart', views.delCart, name='deleteCart'),
    path('showWishList', views.showWishList, name='showWishList'),
    path('removeWishListItem/<product_id>', views.removeWishListItem, name='removeWishListItem'),
    path('saveWishList', views.saveWishList, name='saveWishList'),
]