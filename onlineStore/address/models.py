from django.db import models
from profiles.models import Profile
# Create your models here.
class Address(models.Model):
    profile = models.ForeignKey(Profile, on_delete = models.CASCADE )
    line1 = models.CharField(max_length=100)
    line2= models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=100)


    def __str__(self):
        return self.line1+", "+self.line2+", "+self.city+", "+self.postal_code
