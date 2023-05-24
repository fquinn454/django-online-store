from django.db import models
from django.contrib.auth.models import User
from store.models import Product
from django.db.models.signals import post_save
from django.dispatch import receiver

"""
Profile has a one to one link with the build in User model. 
The built in User model is used for for authentication.
The Profile model stores addidtional data for the user's cart and user's wishlist
"""
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wishlist = models.ManyToManyField(Product, related_name='wishlist', blank=True)
    cart = models.ManyToManyField(Product, related_name='cart', blank=True)

    # return user.username 
    def __str__(self):
        return self.user.username
    
    # Automatically create a Profile instance when a new User instance is created
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    # Save the Profile to DB when a user is created
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    # Display a user's wishlist 
    def getWishlistProducts(request):
        if not request.user.is_authenticated:
            productsToGet = request.session.get('wishlist', [])
            if len(productsToGet) > 0:
                products = []
                for product in productsToGet:
                    products.append(Product.objects.get(id=product))
                return products
            else:
                products = []
            return products
        else:
            products = []
            productsToGet = request.session.get('wishlist', [])
            for product in productsToGet:
                products.append(Product.objects.get(id=product))
            profile = Profile.objects.get(user = request.user)
            for product in profile.wishlist.all():
                products.append(product)
            return products
        
    # Add a product to user wishlist
    def addProductToWishlist(request, product_id):
        if not request.user.is_authenticated:
            wishlist = request.session.get('wishlist', [])
            wishlist.append(product_id)
            # use set to get unique product_ids
            wishlist = set(wishlist) 
            # session storage can not be set
            wishlist = list(wishlist)
            request.session['wishlist'] = wishlist
            request.session.save()
        else:
            profile = Profile.objects.get(user = request.user)
            product = Product.objects.get(id = product_id)
            profile.wishlist.add(product)
    
    # Delete item from user wishlist
    def removeProductFromWishlist(request, product_id):
        if not request.user.is_authenticated:
            wishlist = request.session.get('wishlist', [])
            wishlist.remove(product_id)
            # use set to get unique product_ids
            wishlist = set(wishlist) 
            # session storage can not be set
            wishlist = list(wishlist)
            request.session['wishlist'] = wishlist
            request.session.save()
        else:
            profile = Profile.objects.get(user = request.user)
            product = Product.objects.get(id = product_id)
            profile.wishlist.remove(product)

    # Deletes all products from a user's wish-list
    def deleteWishList(request):
        if not request.user.is_authenticated:
            wishlist = request.session.get('wishlist', [])
            wishlist = []
            request.session['wishlist'] = wishlist
            request.session.save()
        else:
            profile = Profile.objects.get(user = request.user)
            profile.wishlist.clear()

    # Display a user's cart
    def getCartItems(request):
        if not request.user.is_authenticated:
            productsToGet = request.session.get('cart', [])
            if len(productsToGet) > 0:
                products = []
                for product in productsToGet:
                    products.append(Product.objects.get(id=product))
                return products
            else:
                products = []
            return products
        else:
            products = []
            productsToGet = request.session.get('cart', [])
            for product in productsToGet:
                products.append(Product.objects.get(id=product))
            profile = Profile.objects.get(user = request.user)
            for product in profile.cart.all():
                products.append(product)
            return products

    # Adds product to user cart
    def addProductToCart(request, product_id):
        if not request.user.is_authenticated:
            cart = request.session.get('cart', [])
            cart.append(product_id)
            # use set to get unique product_ids
            cart = set(cart) 
            # session storage can not be set
            cart = list(cart)
            request.session['cart'] = cart
            request.session.save()
        else:
            profile = Profile.objects.get(user = request.user)
            product = Product.objects.get(id = product_id)
            profile.cart.add(product)
        
    # Removes an item from a user's cart
    def removeProductFromCart(request, product_id):
        if not request.user.is_authenticated:
            cart = request.session.get('cart', [])
            cart.remove(product_id)
            request.session['cart'] = cart
            request.session.save()
        else:
            profile = Profile.objects.get(user = request.user)
            product = Product.objects.get(id = product_id)
            profile.cart.remove(product)

    # Sum the cost of all the items in a user's cart    
    def sumCart(request):
        if request.user.is_authenticated:
            profile = Profile.objects.get(user = request.user)
            products = profile.cart.all()
        else:
            products = []
            productsToGet = request.session.get('cart', [])
            for product in productsToGet:
                products.append(Product.objects.get(id=product))
        sum = 0
        for product in products:
            sum += product.price 
        return sum







    


