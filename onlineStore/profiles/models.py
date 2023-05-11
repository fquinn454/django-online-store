from django.db import models
from django.contrib.auth.models import User
from store.models import Product
# from django.contrib.auth.decorators import login_required

# Create your models here.
class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, null=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.user.username
    
    def wishlist_add(request):
        try:
            Wishlist.objects.get(id = request.user.id)
        except:
            Wishlist.objects.create(user = request.user)
        
        for product in request.session.get('favourites', []):
            request.user.wishlist.products.add(product)

