from django.db import models

# Create your models here.
from profiles.models import Profile, ProductSet
from address.models import Address

# Create your models here.
class Order(models.Model):
    profile = models.ForeignKey(Profile, on_delete = models.CASCADE )
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    productsets = models.ManyToManyField(ProductSet)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Order Number: "+str(self.id)


