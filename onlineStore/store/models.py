from django.db import models

# Create your models here.
class Image(models.Model):
    name = models.CharField(max_length = 10)
    link = models.CharField(max_length=100)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name

class Product(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    thumbnail = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    images = models.ManyToManyField(Image)
    rating = models.FloatField()
    stock = models.IntegerField()
    discount = models.FloatField()

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.brand + " " +self.title

