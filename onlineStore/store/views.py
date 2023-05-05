from django.http import HttpResponse
from django.shortcuts import render
from .models import Product, Image

def index(request):
    return render(request, "index.html")

def welcome(request):
    return render(request, "welcome.html")

def products(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, "products.html", context)

def showProduct(request, product_id):
    product = Product.objects.get(pk=product_id)
    images = product.images.all()
    context = {'product': product, 'images': images }
    return render(request, "showProduct.html", context)
