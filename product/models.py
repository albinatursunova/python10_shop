from django.db import models
from django.urls import reverse_lazy


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, primary_key=True)

    def __str__(self):
        return self.name

# варианты on_delete:
# CASCADE - при удалении категории, удалятся все продукты из этой категории
# SET_NULL - при удалениии категории, занчание поля caregory для всех продуктов станет null
# SET_DEFAULT - при удалениии категории, занчание поля caregory в связанных продуктах заменяет на дефолтное
# PROTECT
# RESTRICT
# не дают удалить категорию, если в ней есть продукты
# DO_NOTHING - отсутсвие действия
# SET - не рассматриваем

class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('product_details', kwargs={'pk': self.id})


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products', null=True, blank=True)

# ORM (Object-Relational Mapping)