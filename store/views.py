from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from .models import Product, OrderItem, Collection, Reviews
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer

# Create your views here.
@api_view(['GET', 'POST'])
def collection_list(request):
	if request.method == 'GET':
		collection = Collection.objects.all()
		serializer = CollectionSerializer(collection, many=True)
		return Response(serializer.data)
	elif request.method == 'POST':
		collection = CollectionSerializer(data=request.data)
		collection.is_valid(raise_exception=True)
		collection.save()
		return Response(collection.data, status=status.HTTP_201_CREATED)

# Create your views here.
class ProductViewSet(ModelViewSet):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer

	def destroy(self, request, *args, **kwargs):
		if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
			return Response({'error': 'product can not be deleted'})
		return  super().destroy(request, *args, **kwargs)

class ReviewViewSet(ModelViewSet):
	queryset = Reviews.objects.all()
	serializer_class = ReviewSerializer

	def get_serializer_context(self):
		return {'product_id': self.kwargs['product_pk']}