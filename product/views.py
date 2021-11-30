""" Documentation APIView https://www.django-rest-framework.org/api-guide/generic-views/#genericapiview"""
from django.db.models import Q
from django.http import Http404

# APIView é uma classe do DRF que herda de View e que traz algumas configurações específicas para transformá-las em APIs, como métodos get() e post().
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


class LatestProductsList(APIView):
    # Função pronta do APIView 
    def get(self, request, format=None):
        products = Product.objects.all()[0:4]
        # Configura qual Serializer deversá ser usado para consumir dados que chegam à API e produzir dados que serão enviados como resposta.
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ProductDetail(APIView):
    #  Retorna uma instância de objeto que deve ser usada para visualizações detalhadas.
    def get_object(self, category_slug, product_slug):
        try:
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
        except Product.DoesNotExist:
            raise Http404
    
    def get(self, request, category_slug, product_slug, format=None):
        product = self.get_object(category_slug, product_slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


class CategoryDetail(APIView):
    def get_object(self, category_slug):
        try:
            return Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            raise Http404
    
    def get(self, request, category_slug, format=None):
        category = self.get_object(category_slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data)


@api_view(['POST'])
def search(request):
    query = request.data.get('query', '')

    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    else:
        return Response({"products": []})