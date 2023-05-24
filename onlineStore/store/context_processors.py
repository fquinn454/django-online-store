from profiles.models import Profile
from .models import Product

"""
returns a count of the number of items in the 
user wishlist and the user cart. For use in the 
nav bar badges on all pages 
"""
def getCounts(request):
    if not request.user.is_authenticated:
        # get session cart and wishlist integer lists
        cart = request.session.get('cart', [])
        wishlist = request.session.get('wishlist', [])
        # use set to get unique product_ids
        wishlist = set(wishlist)
        cart = set(cart)  
        wishlist = list(wishlist)
        cart = list(cart)
        wishlistLength = len(wishlist)
        cartLength = len(cart)
        return {'cartLength': cartLength, 'wishlistLength': wishlistLength}
    else:
        # get the current session variables for wishlist and cart
        session_wishlist = request.session.get('wishlist', [])
        session_wishlist = set(session_wishlist)
        session_wishlist = list(session_wishlist)
        session_cart = request.session.get('cart', [])
        session_cart = set(session_cart)
        session_cart = list(session_cart)
        # add them to the now logged in user's wishlist and cart
        profile = Profile.objects.get(user = request.user)
        for id_num in session_wishlist:
            profile.wishlist.add(Product.objects.get(pk = id_num))
        
        for id_num in session_cart:
            profile.cart.add(Product.objects.get(pk = id_num))
        
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