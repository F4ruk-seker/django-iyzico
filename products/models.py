from django.db import models


class ProductModel(models.Model):
    class ItemType(models.TextChoices):
        PHYSICAL = 'P', 'PHYSICAL'
        VIRTUAL = 'v', 'VIRTUAL'

    name = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    item_type = models.CharField(max_length=1, default=ItemType.PHYSICAL, choices=ItemType)
    price = models.FloatField(default=.0)
    ...


class BasketModel(models.Model):
    # user = OneToOne
    products = models.ManyToManyField('ProductModel', default=None, blank=True)

    def get_products(self):
        return self.products.all()

    def get_total_price(self):
        total_price = self.products.aggregate(total_price=models.Sum('price'))['total_price']
        return total_price or 0.0


