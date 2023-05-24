# from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Product, Image
from profiles.models import Profile

# HOMEPAGE
# returns homepage
def index(request):
    return render(request, "index.html")

# PRODUCTS
# returns all products in database
def products(request):
    products = Product.objects.all()
    categories = map(lambda x: x[1], Product.CATEGORIES)
    brands = map(lambda x: x[1], Product.BRANDS)
    context = {'products': products, 'categories':categories, 'brands': brands}
    return render(request, "products.html", context)

# returns all products with particular category
def getCategory(request, category):
    products = Product.objects.filter(category = category)
    categories = map(lambda x: x[1], Product.CATEGORIES)
    brands = map(lambda x: x[1], Product.BRANDS)
    context = {'products': products, 'categories':categories, 'brands': brands}
    return render(request, "products.html", context)

# returns all products with particular brand
def getBrand(request, brand):
    products = Product.objects.filter(brand = brand)
    categories = map(lambda x: x[1], Product.CATEGORIES)
    brands = map(lambda x: x[1], Product.BRANDS)
    context = {'products': products, 'categories':categories, 'brands': brands}
    return render(request, "products.html", context)

# returns product info for single product 
def showProduct(request, product_id):
    product = Product.objects.get(pk=product_id)
    images = Image.objects.filter(product = product_id)
    context = {'product': product, 'images': images }
    return render(request, "showProduct.html", context)

# WISHLIST
# returns user Wish List 
def showWishList(request):
   products = Profile.getWishlistProducts(request)
   context = {'products': products}
   return render(request, "showWishList.html", context)

# returns /wishlist after user adds item to wishlish
def addFavourite(request, product_id):
    Profile.addProductToWishlist(request, product_id)
    return redirect(request.META.get('HTTP_REFERER', '/'))

# returns /wishlist after user deletes a product from wishlish
def removeWishListItem(request, product_id):
    Profile.removeProductFromWishlist(request, product_id)
    return redirect(request.META.get('HTTP_REFERER', '/'))

# returns /wishlist after user deletes all products in wish list
def delWishList(request):
    Profile.deleteWishList(request)
    return redirect(request.META.get('HTTP_REFERER', '/'))

# CART
# returns user cart
def showCart(request):
   products = Profile.getCartItems(request)
   total = Profile.sumCart(request)
   context = {'products': products, 'total': total}
   return render(request, "showcart.html", context)

# returns showCart.html after user add product to cart
def addToCart(request, product_id):
    Profile.addProductToCart(request, product_id)
    return redirect(request.META.get('HTTP_REFERER', '/'))

# returns showcart.html after user deletes a product from cart
def removeCartItem(request, product_id):
    Profile.removeProductFromCart(request, product_id)
    return redirect(request.META.get('HTTP_REFERER', '/'))

