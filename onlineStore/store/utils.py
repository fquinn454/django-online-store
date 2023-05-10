def getSessionVariableLengths(request):
    favourites = request.session.get('favourites', [])
    favourites = set(favourites) 
    favouritesLength = len(favourites)
    cart = request.session.get('cart', [])
    cartLength = len(cart)
    cart = set(cart)
    return (favouritesLength, cartLength)

def deleteUserWishList(request):
    favourites = request.session.get('favourites', [])
    favourites = []
    request.session['favourites'] = favourites
    request.session.save()

def deleteUserCart(request):
    favourites = request.session.get('cart', [])
    favourites = []
    request.session['cart'] = favourites
    request.session.save()

def addUserFavourite(request, product_id):
    favourites = request.session.get('favourites', [])
    favourites.append(product_id)
    favourites = set(favourites) 
    favourites = list(favourites)
    request.session['favourites'] = favourites
    request.session.save()

def removeUserWishListItem(request, product_id):
    favourites = request.session.get('favourites', [])
    favourites.remove(product_id)
    favourites = set(favourites) 
    favourites = list(favourites)
    request.session['favourites'] = favourites
    request.session.save()