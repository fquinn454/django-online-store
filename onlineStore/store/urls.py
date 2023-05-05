from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("products", views.products, name="products"),
    path("products/<product_id>", views.showProduct, name="showProduct"),

]