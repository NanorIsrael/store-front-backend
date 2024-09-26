from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from .models import Product, OrderItem, Collection, Reviews, Cart, CartItem
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer, CartSerializer \
	, CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer
# Create your views here.
class CollectionViewSet(ModelViewSet):
	queryset = Collection.objects.all()
	serializer_class = CollectionSerializer

# Create your views here.
class ProductViewSet(ModelViewSet):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ['collection_id']


	def destroy(self, request, *args, **kwargs):
		if OrderItem.objects.filter(product_id=self.kwargs['pk']).count() > 0:
			return Response({'error': 'product can not be deleted'})
		return  super().destroy(request, *args, **kwargs)

class ReviewViewSet(ModelViewSet):
	# queryset = Reviews.objects.all()
	serializer_class = ReviewSerializer

	def get_queryset(self):
		return Reviews.objects.filter(product_id=self.kwargs.get('product_pk'))

	def get_serializer_context(self):
		return {'product_id': self.kwargs['product_pk']}


class CartViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
	queryset = Cart.objects.all()
	serializer_class = CartSerializer

class CartItemViewSet(ModelViewSet):
	http_method_names = ['get', 'post', 'patch', 'delete']
	def get_serializer_class(self):
		if self.request.method == 'POST':
			return AddCartItemSerializer
		if self.request.method == 'PATCH':
			return UpdateCartItemSerializer
		return CartItemSerializer

	def get_queryset(self):
		print(self.kwargs)
		# print(CartItemSerializer(CartItem.objects.all()[0]))
		queryset = CartItem.objects.filter(cart_id=self.kwargs.get('cart_pk')).select_related('product')
		return queryset

	def get_serializer_context(self):
		return {'cart_id': self.kwargs['cart_pk']}
