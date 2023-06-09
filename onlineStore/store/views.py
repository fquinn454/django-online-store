from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Product, Image
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from profiles.models import Profile, ProductSet
from address.models import Address
from order.models import Order
import stripe

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
@login_required
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
                client_reference_id=request.user.id if request.user.is_authenticated else None,
                shipping_address_collection={"allowed_countries": ["GB"]},
                payment_method_types =['card'],
                line_items = items,
                mode='payment',
                success_url= 'https://quinnf.pythonanywhere.com/success',
                cancel_url = 'https://quinnf.pythonanywhere.com/cancelled',
            )

            return JsonResponse({'sessionId': session['id']})

        except Exception as e:
            return JsonResponse({'error': str(e)})

def success(request):
    profile = Profile.objects.get(user = request.user)
    orders = Order.objects.filter(profile = profile).order_by('-id')
    order = orders[0]
    return render(request, "success.html", {'order': order})

def showOrders(request):
    profile = Profile.objects.get(user = request.user)
    orders = Order.objects.filter(profile = profile).order_by('-id')
    username = request.user.username
    context = {'profile':profile, 'orders':orders, 'username':username}
    return render(request, "showOrders.html", context)

def showAddresses(request):
    addresses = Address.objects.filter(profile = Profile.objects.get(user = request.user))
    username = request.user.username
    context = {'addresses':addresses, 'username':username}
    return render(request, "showAddresses.html", context)

def cancelled(request):
    return render(request, "cancelled.html")

@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        print("Payment was successful.")
        session = stripe.checkout.Session.retrieve(
          event['data']['object']['id'],
          expand=['line_items'],
        )

        try:
            addresses = Address.objects.filter(profile = Profile.objects.get(user = User.objects.get(id = session.client_reference_id)))
            for item in addresses:
                if item.line1 == session.customer_details.address.line1:
                    order_address_to_save = item

            order_address = order_address_to_save

        except:
            order_address = Address.objects.create(
                profile=Profile.objects.get(user = session.client_reference_id),
                line1=session.customer_details.address.line1,
                line2=session.customer_details.address.line2,
                city=session.customer_details.address.city,
                postal_code=session.customer_details.address.postal_code
            )

            order_address.save()

        order = Order.objects.create(
            profile=Profile.objects.get(user = User.objects.get(id = session.client_reference_id)),
            address = order_address
        )

        order.save()

        for item in session.line_items:

            user=User.objects.get(id = session.client_reference_id)
            product = Product.objects.get(title = item.description)
            quantity = item.quantity

            try:
                productSet = ProductSet.objects.get(
                user=user,
                product = product,
                quantity = quantity
            )

            except:
                productSet = ProductSet.objects.create(
                user=user,
                product = product,
                quantity = quantity
            )
            product.stock -= quantity
            product.save()
            order.productsets.add(productSet)
            order.save()

        profile=Profile.objects.get(user = User.objects.get(id = session.client_reference_id))
        profile.cart.clear()

        return HttpResponse(status=200)



