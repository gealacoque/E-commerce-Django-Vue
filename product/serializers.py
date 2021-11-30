# Eles servem para traduzir entidades complexas, como querysets e instâncias de classes em 
# representações simples que podem ser usadas no tráfego da web, como JSON e XML.

from rest_framework import serializers

from .models import Product, Category

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        # Define qual modelo esse serializer deve serializar.
        model = Product
        # Define os campos que serão serializados.
        fields = (
            "id",
            "name",
            "get_absolute_url",
            "description",
            "price",
            "get_image",
            "get_thumbnail"
        )


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "get_absolute_url",
            "products",
        )
