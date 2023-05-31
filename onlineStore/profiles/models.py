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
class ProductSet(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE )
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.product.title+" x "+str(self.quantity)
    
    def getTotalCost(self):
        return self.product.price * self.quantity
    
    # Display a user's cart
    def getCartItems(request):
        if request.user.is_authenticated:
            profile = Profile.objects.get(user = request.user)
            productsets = profile.cart.all()
            return productsets
        else:
            cart = request.session.get('cart', [])
            productsets = []
            if cart:
                for item in cart:
                    product = Product.objects.get(id = item[0])
                    productset = {'product': product, 'quantity': item[1] }
                    cost = product.price * item[1]
                    productset['getTotalCost'] = cost
                    productsets.append(productset)
                return productsets
            else:
                return productsets

    # Adds product to user cart
    def addProductToCart(request, product_id):
        if request.user.is_authenticated:
            profile = Profile.objects.get(user = request.user)
            product = Product.objects.get(id = product_id)
            try:
                productset = ProductSet.objects.get(user = request.user, product = product)
                productset.quantity = 1
                productset.save()
                profile.cart.add(productset)
            except:
                profile.cart.add(ProductSet.objects.create(user = request.user, product = product))
        else:
            cart = request.session.get('cart', [])
            cart.append((int(product_id), int(1)))
            request.session['cart'] = cart
            request.session.save()


    # Removes an item from a user's cart
    def removeProductFromCart(request, product_id):
        if request.user.is_authenticated:
            profile = Profile.objects.get(user = request.user)
            product = Product.objects.get(id = product_id)
            profile.cart.remove(ProductSet.objects.get(user = request.user, product = product))
            profile.save()
        else:
            cart = request.session.get('cart', [])
            for item in cart:
                if item[0] == int(product_id):
                    cart.remove(item)
                    request.session['cart'] = cart
                    request.session.save()

    # Sum the cost of all the items in a user's cart    
    def sumCart(request):
        if request.user.is_authenticated:
            profile = Profile.objects.get(user = request.user)
            productsets = profile.cart.all()
            sum = 0
            for productset in productsets:
                sum += productset.product.price * productset.quantity
            return sum
        else:
            cart = request.session.get('cart', [])
            if cart:
                sum = 0
                for item in cart:
                    product = Product.objects.get(id = item[0])
                    sum += product.price * item[1]
                return sum

    def increment(request, product_id):
        if request.user.is_authenticated:
            profile = Profile.objects.get(user = request.user)
            product = Product.objects.get(id = product_id)
            productsets = profile.cart.all()
            productset = productsets.get(user = request.user, product = product)
            productset.quantity += 1
            productset.save()
        else:  
            cart = request.session.get('cart', [])
            for item in cart:
                if item[0] == int(product_id):
                    item[1] += 1
                    request.session['cart'] = cart
                    request.session.save()

    def decrement(request, product_id):
        if request.user.is_authenticated:
            profile = Profile.objects.get(user = request.user)
            product = Product.objects.get(id = product_id)
            productsets = profile.cart.all()
            productset = productsets.get(user = request.user, product = product)
            if productset.quantity > 1:
                productset.quantity -= 1
                productset.save()
        else:  
            cart = request.session.get('cart', [])
            for item in cart:
                if item[0] == int(product_id):
                    if item[1] > 1:
                        item[1] -= 1
                        request.session['cart'] = cart
                        request.session.save()
                

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wishlist = models.ManyToManyField(Product, related_name='wishlist', blank=True)
    cart = models.ManyToManyField(ProductSet, related_name='cart', blank=True)

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

    







    


