# from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Product, Image
from django.http import JsonResponse
from profiles.models import Profile, ProductSet
import stripe
import json
from django.views.generic.base import TemplateView

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
    productsets = ProductSet.getCartItems(request)
    total = ProductSet.sumCart(request)
    context = {'productsets': productsets, 'total': total }
    return render(request, "showcart.html", context)

# returns showCart.html after user add product to cart
def addToCart(request, product_id):
    ProductSet.addProductToCart(request, product_id)
    return redirect(request.META.get('HTTP_REFERER', '/'))

# returns showcart.html after user deletes a product from cart
def removeCartItem(request, product_id):
    ProductSet.removeProductFromCart(request, product_id)
    return redirect(request.META.get('HTTP_REFERER', '/'))

def increment(request, product_id):
    ProductSet.increment(request, product_id)
    return redirect(request.META.get('HTTP_REFERER', '/'))

def decrement(request, product_id):
    ProductSet.decrement(request, product_id)
    return redirect(request.META.get('HTTP_REFERER', '/'))

# Stripe checkout
@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLIC_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        stripe.api_key = settings.STRIPE_SECRET_KEY
        productsets = ProductSet.getCartItems(request)
        price = 0
        items = []

        for productset in productsets:
            product = productset.product
            price += product.price * productset.quantity

            obj = {
                'price_data': {
                    'currency': 'gbp',
                    'product_data' : {
                        'name': product.title,
                    },
                    'unit_amount': int(product.price*100),
                },
                'quantity': productset.quantity
            }
            items.append(obj)

        try:
            session = stripe.checkout.Session.create(
                payment_method_types =['card'],
                line_items = items,
                mode='payment', 
                success_url= 'http://127.0.0.1:8000/success',
                cancel_url = 'http://127.0.0.1:8000/cancelled'
            )
            return JsonResponse({'sessionId': session['id']})
        
        except Exception as e:
            return JsonResponse({'error': str(e)})

def success(request):
    return render(request, "success.html")

def cancelled(request):
    return render(request, "cancelled.html")