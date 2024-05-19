from rest_framework import serializers
from products.models import ProductModel


class ProductSerializer(serializers.ModelSerializer):
    # id = serializers.Met
    itemType = serializers.SerializerMethodField()
    category1 = serializers.SerializerMethodField()

    def get_itemType(self, obj):
        return obj.get_item_type_display()

    def get_category1(self, obj):
        return obj.category

    class Meta:
        model = ProductModel
        fields: str = '__all__'

