from django.contrib import admin
from .models import ProductModel, BasketModel


admin.site.register(ProductModel)
admin.site.register(BasketModel)

