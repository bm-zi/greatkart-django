from django.db import models
from django.urls import reverse

from category.models import Category

# Create your models here.

class Product(models.Model):
    product_name    = models.CharField(max_length=200, unique=True)
    slug            = models.SlugField(max_length=200, unique=True)
    description     = models.TextField(max_length=500, blank=True)
    price           = models.IntegerField()
    images          = models.ImageField(upload_to='photos/products')
    stock           = models.IntegerField()
    is_available    = models.BooleanField(default=True)
    
    category        = models.ForeignKey(Category, on_delete=models.CASCADE)
    # on_delete=models.CASCADE means whenever a category is deleted, all
    # products attached to that category will be deleted.

    # auto_now_add=True automatically set the field to now when the object is first created.
    created_date = models.DateTimeField(auto_now_add=True)
    # auto_now=True automatically set the field to now every time the object is saved.
    modified_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name
