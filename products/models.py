from django.db import models

'''
{
    'id': 'BI103',
    'name': 'Usb',
    'category1': 'Electronics',
    'category2': 'Usb / Cable',
    'itemType': 'PHYSICAL',
    'price': '0.2'
}
'''


class ProductModel(models.Model):
    name = models.CharField(max_length=50)


