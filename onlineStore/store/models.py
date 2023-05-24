from django.db import models

# Create your models here.
class Product(models.Model):
    CATEGORIES = (
        ('Smartphone', 'Smartphone'),
        ('Laptop', 'Laptop'),
    )

    BRANDS = (
        ('Apple', 'Apple'),
        ('Samsung', 'Samsung'),
        ('OPPO', 'OPPO'),
        ('Huawei', 'Huawei'),
        ('Microsoft', 'Microsoft'),
        ('Infinix', 'Infinix'),
        ('HP', 'HP'),
    )
    id = models.IntegerField(primary_key=True, unique=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    thumbnail = models.CharField(max_length=100)
    brand = models.CharField(max_length=100, choices=BRANDS)
    category = models.CharField(max_length=100, choices=CATEGORIES)
    rating = models.FloatField()
    stock = models.IntegerField()
    discount = models.FloatField()

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.brand + " " +self.title
    

class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length = 10)
    link = models.CharField(max_length=100)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name


