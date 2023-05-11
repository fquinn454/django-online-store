from django.db import models

# Create your models here.
class Product(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    thumbnail = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    rating = models.FloatField()
    stock = models.IntegerField()
    discount = models.FloatField()

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.brand + " " +self.title
    
    def productsToGet(request):
        productsToGet = request.session['favourites']
        products = []
        for product in productsToGet:
            products.append(Product.objects.get(id=product))
        return products

class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length = 10)
    link = models.CharField(max_length=100)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name
