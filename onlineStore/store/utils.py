from profiles.models import User, Profile

""" 
Functions in utils.py are used to work with a
user's wishlist and cart. 
Information about a non-logged in user's
wish-list and cart is stored in session storage.  
The user's wishlist is a list of product id numbers.  
The user's cart is another separate list of product id numbers.
Information about a logged in user's cart and wishlist is stored in the database
"""

"""
Returns the number of items in user's wish-list and cart.
Function used by several views to render the correct count information 
in wish-list and cart badge icons.
"""
def getSessionVariableLengths(request):
    favourites = request.session.get('favourites', [])
    # use set to get unique product_ids
    favourites = set(favourites) 
    favouritesLength = len(favourites)
    cart = request.session.get('cart', [])
    cartLength = len(cart)
    cart = set(cart)
    return (favouritesLength, cartLength)

""" 
Deletes all products from the non-logged in user's wish-list
"""
def deleteUserWishList(request):
    favourites = request.session.get('favourites', [])
    favourites = []
    request.session['favourites'] = favourites
    request.session.save()

""" 
Deletes all items from the non-logged in user's cart
"""
def deleteUserCart(request):
    favourites = request.session.get('cart', [])
    favourites = []
    request.session['cart'] = favourites
    request.session.save()

""" 
Adds an int (product_id) to the non-logged in user's 
wish-list (favourites). This list is passed to a view
to render user wishlist.
"""
def addUserFavourite(request, product_id):
    favourites = request.session.get('favourites', [])
    favourites.append(product_id)
    # use set to get unique product_ids
    favourites = set(favourites) 
    # session storage can not be set
    favourites = list(favourites)
    request.session['favourites'] = favourites
    request.session.save()

""" 
Removes an int (product_id) to the non-logged in user's 
wish-list (favourites). This list is passed to a view
to render user wishlist.
"""
def removeUserWishListItem(request, product_id):
    favourites = request.session.get('favourites', [])
    favourites.remove(product_id)
    # use set to get unique product_ids
    favourites = set(favourites) 
    # session storage can not be set
    favourites = list(favourites)
    request.session['favourites'] = favourites
    request.session.save()


""" 
Saves a logged in user's wishlist to the database
"""
def wishlist_add(request):
    user = User.objects.get(username = request.user.username)
    profile = Profile.objects.get(user = user)
    products = request.session.get('favourites', [])
    for product in products:
        profile.wishlist.add(product)