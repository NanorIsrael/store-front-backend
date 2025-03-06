from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin

from common.permissions import IsAdminOrReadOnly
from .models import Product, OrderItem, Collection, Reviews, Cart, CartItem, Customer, Order
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer, CartSerializer \
	, CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer, CustomerSerializer \
	, OrderSerializer, CreateOrderSerializer, updateOrderSerialzer

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
	permission_classes = [IsAdminOrReadOnly]

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


class CustomerViewSet(CreateModelMixin,RetrieveModelMixin,UpdateModelMixin, GenericViewSet):
	queryset = Customer.objects.all()
	serializer_class = CustomerSerializer
	permission_classes = [IsAuthenticated]
	# def get_permissions(self):
	# 	if self.request.method == 'GET':
	# 		return [AllowAny()]
	# 	return [IsAuthenticated()]

	@action(detail=False, methods=['GET', 'PATCH', 'PUT'])
	def me(self, request):
		query, created = Customer.objects.get_or_create(user_id=request.user.id)
		if request.method == 'GET':
			customer = CustomerSerializer(query);
			return Response(customer.data)
		if request.method == 'PUT':
			serializer = CustomerSerializer(query, data=request.data);
			serializer.is_valid(raise_exception=True)
			serializer.save()
			return Response(serializer.data)
		else:
			pass
			# return Response(created)

class OrdersViewSet(CreateModelMixin,RetrieveModelMixin,UpdateModelMixin, GenericViewSet):
	http_method_names = ['get', 'patch', 'delete', 'head', 'post', 'options']
	def get_permissions(self):
		if self.request.method in ['PATCH', 'DELETE']:
			return [IsAdminUser()]
		return [IsAuthenticated()]

	def create(self, request, *args, **kwargs):
		serializer = CreateOrderSerializer(request.data, context={'user_id': self.request.user})
		serializer.validated_data(raise_exeption=True)
		order = serializer.save()
		serialized_order = OrderSerializer(order)
		return Response(serialized_order.data)

	def get_queryset(self):
		user = self.request.user
		if user.is_staff:
			return Order.objects.all()
		customer_id = Customer.objects.only('id').get(user_id=user.id)
		Order.objects.filter(customer_id=customer_id)

	def get_serializer_class(self):
		if self.request.method == 'POST':
			return CreateOrderSerializer
		if self.request.method == 'PATCH':
			return updateOrderSerialzer
		return OrderSerializer
	