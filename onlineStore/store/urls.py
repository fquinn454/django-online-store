from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("products", views.products, name="products"),
    path("getCategory/<category>", views.getCategory, name="getCategory"),
    path("getBrand/<brand>", views.getBrand, name="getBrand"),
    path("products/<product_id>", views.showProduct, name="showProduct"),
    path('addFavourite/<product_id>', views.addFavourite, name='addFavourite'),
    path('addToCart/<product_id>', views.addToCart, name='addToCart'),
    path('deleteWishList', views.delWishList, name='deleteWishList'),
    path('showWishList', views.showWishList, name='showWishList'),
    path('removeWishListItem/<product_id>', views.removeWishListItem, name='removeWishListItem'),
    path('showcart', views.showCart, name="showcart"),
    path('removeCartItem/<product_id>', views.removeCartItem, name='removeCartItem')
]