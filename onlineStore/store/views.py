from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Product
from .utils import *

def index(request):
    lengths = getSessionVariableLengths(request)
    products = Product.objects.all()
    context = {'products': products, 'favouritesLength': lengths[0], 'cartLength': lengths[1]}
    return render(request, "index.html", context)

def products(request):
    lengths = getSessionVariableLengths(request)
    products = Product.objects.all()
    context = {'products': products, 'favouritesLength': lengths[0], 'cartLength': lengths[1]}
    return render(request, "products.html", context)

def showProduct(request, product_id):
    lengths = getSessionVariableLengths(request)
    product = Product.objects.get(pk=product_id)
    images = product.images.all()
    context = {'product': product, 'images': images,'favouritesLength': lengths[0], 'cartLength': lengths[1] }
    return render(request, "showProduct.html", context)

def addFavourite(request, product_id):
    addUserFavourite(request, product_id)
    return redirect(request.META.get('HTTP_REFERER', '/'))

def delWishList(request):
    deleteUserWishList(request)
    return redirect(request.META.get('HTTP_REFERER', '/'))

def delCart(request):
    deleteUserCart(request)
    return redirect(request.META.get('HTTP_REFERER', '/home'))

def addToCart(request, product_id):
    cart = request.session.get('cart', [])
    cart.append(product_id)
    request.session['cart'] = cart
    request.session.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

def showWishList(request):
   lengths = getSessionVariableLengths(request)
   products = Product.productsToGet(request)
   context = {'products': products, 'favouritesLength': lengths[0], 'cartLength': lengths[1]}
   return render(request, "showWishList.html", context)

def removeWishListItem(request, product_id):
    removeUserWishListItem(request, product_id)
    return redirect(request.META.get('HTTP_REFERER', '/'))