from django.db import models

# Create your models here.
from profiles.models import Profile
from store.models import Product

# Create your models here.
class Order(models.Model):
    profile = models.ForeignKey(Profile, on_delete = models.CASCADE )
    products = models.ManyToManyField(Product)
    