from django.db import models

# Create your models here.
from profiles.models import Profile, ProductSet
from address.models import Address
from datetime import date

# Create your models here.
class Order(models.Model):
    profile = models.ForeignKey(Profile, on_delete = models.CASCADE )
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    productsets = models.ManyToManyField(ProductSet)
    date = models.DateField(default = date.today())

    def __str__(self):
        return "Order: "+str(self.id)+", Date: "+str(self.date.day)+" "+str(self.date.strftime("%B"))+", Email: "+self.profile.user.email+", Postcode "+str(self.address.postal_code)


