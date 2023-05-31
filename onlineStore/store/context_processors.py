from profiles.models import Profile, ProductSet
from .models import Product

"""
The user's cart and wishlist are stored in the db
when the user is logged in, otherwise this information 
is stored as product_ids(intergers) stored in session storage.

Returns a count of the number of items in the 
user wishlist and the user cart. 
These counts are used in the badges above the cart and 
heart icons in the navon all pages.

"""
def getCounts(request):
    if not request.user.is_authenticated:
        # get session cart and wishlist integer lists
        cart = request.session.get('cart', {})
        wishlist = request.session.get('wishlist', [])
        # use set to get unique product_ids
        wishlist = set(wishlist)
        wishlist = list(wishlist)
        wishlistLength = len(wishlist)
        cartLength = len(cart)
        return {'cartLength': cartLength, 'wishlistLength': wishlistLength}
    else:
        # get the current session variables for wishlist and cart
        session_wishlist = request.session.get('wishlist', [])
        session_wishlist = set(session_wishlist)
        session_wishlist = list(session_wishlist)
        session_cart = request.session.get('cart', [])
        # add them to the now logged in user's wishlist and cart
        profile = Profile.objects.get(user = request.user)
        for id_num in session_wishlist:
            profile.wishlist.add(Product.objects.get(pk = id_num))
        
        for id_num in session_cart:
            productSet = ProductSet.objects.create(user= request.user, product = Product.objects.get(pk = id_num[0]))
            profile.cart.add(productSet)
        
        # get the count of cart and wishlish for nav badges
        cart = profile.cart.all()
        cartLength = len(cart)
        wishlist = profile.wishlist.all()
        wishlistLength = len(wishlist)

        # reset session variables 
        wishlist = []
        request.session['wishlist'] = wishlist
        request.session.save()
        cart = []
        request.session['cart'] = cart
        request.session.save()
        return {'cartLength': cartLength, 'wishlistLength': wishlistLength}