# from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Image
from django.contrib.auth.models import User
from profiles.models import Profile
from .utils import *

# HOMEPAGE
# returns homepage
def index(request):
    lengths = getSessionVariableLengths(request)
    context = {'favouritesLength': lengths[0], 'cartLength': lengths[1]}
    return render(request, "index.html", context)

# PRODUCTS
# returns all products in database
def products(request):
    lengths = getSessionVariableLengths(request)
    products = Product.objects.all()
    context = {'products': products, 'favouritesLength': lengths[0], 'cartLength': lengths[1]}
    return render(request, "products.html", context)

# returns product info for single product 
def showProduct(request, product_id):
    lengths = getSessionVariableLengths(request)
    product = Product.objects.get(pk=product_id)
    images = Image.objects.filter(product = product_id)
    context = {'product': product, 'images': images,'favouritesLength': lengths[0], 'cartLength': lengths[1] }
    return render(request, "showProduct.html", context)


# WISHLIST
# returns user Wish List 
def showWishList(request):
   lengths = getSessionVariableLengths(request)
   try:
    products = Product.productsToGet(request)
    context = {'products': products, 'favouritesLength': lengths[0], 'cartLength': lengths[1]}
   except:
       context = {'products' : [], 'favouritesLength': lengths[0], 'cartLength': lengths[1] }
   
   return render(request, "showWishList.html", context)

# returns showWishList.html after user adds item to wishlish
def addFavourite(request, product_id):
    addUserFavourite(request, product_id)
    return redirect(request.META.get('HTTP_REFERER', '/'))

# returns showWishList.html after user deletes a product from wishlish
def removeWishListItem(request, product_id):
    removeUserWishListItem(request, product_id)
    return redirect(request.META.get('HTTP_REFERER', '/'))

# returns showWishList.html after user deletes all products in wish list
def delWishList(request):
    deleteUserWishList(request)
    return redirect(request.META.get('HTTP_REFERER', '/'))


# Saves a user's wishlist to their account - must be logged in
@login_required(login_url='/profiles/login')
def saveWishList(request):
    wishlist_add(request)
    return redirect(request.META.get('HTTP_REFERER', '/'))

# CART
# returns showCart.html after user add product to cart
def addToCart(request, product_id):
    cart = request.session.get('cart', [])
    cart.append(product_id)
    request.session['cart'] = cart
    request.session.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

# returns showCart.html after user deletes all products in cart
def delCart(request):
    deleteUserCart(request)
    return redirect(request.META.get('HTTP_REFERER', '/'))


