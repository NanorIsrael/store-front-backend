from django.db import transaction
from decimal import Decimal
from rest_framework import serializers
from .models import Product, Collection, Reviews, Cart, CartItem, Customer, Order \
, OrderItem

class CollectionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Collection
		fields = ['id', 'title']
  
 
class ProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = ['id', 'title', 'unit_price', 'price_with_tax', 'collection', 'inventory']

	price_with_tax = serializers.SerializerMethodField(method_name='process_tax')
	
	def process_tax(self, product: Product):
		return product.unit_price * Decimal(1.1)

class ReviewSerializer(serializers.ModelSerializer):
	# product = serializers.ReadOnlyField()
	class Meta:
		model = Reviews
		fields = ['id', 'name', 'description', 'date']

	def create(self, validated_data):
		product_id = self.context.get('product_id');
		return Reviews.objects.create(product_id=product_id, **validated_data)

class CartItemSerializer(serializers.ModelSerializer):
	product = ProductSerializer(read_only=True)
	total_price = serializers.SerializerMethodField(method_name='item_total_price')
	
	def item_total_price(self, cart_item: CartItem):
		return cart_item.quantity * cart_item.product.unit_price

	class Meta:
		model = CartItem
		fields = ['id', 'product', 'quantity', 'total_price']


class CartSerializer(serializers.ModelSerializer):
	id = serializers.UUIDField(read_only=True)
	items = CartItemSerializer(many=True)
	# total = serializers.DecimalField(max_digits=6, decimal_places=2)

	# def total_charge(self, cart: Cart):
	# 	return self.total += 1

	class Meta:
		model = Cart
		fields = ['id', 'items']

class AddCartItemSerializer(serializers.ModelSerializer):
	product_id = serializers.IntegerField()

	def validate_product_id(self, product_id):
		if not Product.objects.filter(pk=product_id).exists():
			raise serializers.ValidationError('No product with the given id found.')
		return product_id
	
	def save(self, **kwargs):
		cart_id = self.context.get('cart_id')
		product_id = self.validated_data.get('product_id')
		quantity = self.validated_data.get('quantity')

		try:
			cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
			cart_item.quantity += quantity
			cart_item.save()
			self.instance = cart_item
		except CartItem.DoesNotExist:
			self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)
			return self.instance

	class Meta:
		model = CartItem
		fields = ['id', 'product_id', 'quantity']

class UpdateCartItemSerializer(serializers.ModelSerializer):
	class Meta:
		model = CartItem
		fields = ['quantity']

class CustomerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Customer
		fields = ['id', 'birth_date', 'phone', 'first_name', 'membership']

class SimpleProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = ['id', 'title', 'unit_price']

class OrderItemSerializer(serializers.ModelSerializer):
	product = ProductSerializer
	class Meta:
		model = OrderItem
		fields = ['id', 'product', 'quantity', 'unit_price']

class OrderSerializer(serializers.ModelSerializer):
	items = OrderItemSerializer(many=True)
	class Meta:
		model = Order
		fields = ['id', 'customer', 'placed_at', 'items']

class CreateOrderSerializer(serializers.ModelSerializer):
	cart_id = serializers.UUIDField()

	def validate_cart_id(self, cart_id):
		if not Cart.objects.filter(pk=cart_id).exists():
			serializers.ValidationError('No cart with the given id was found')
		return cart_id

	def save(self, **kwargs):
		with transaction.atomic():
			cart_id = self.validated_data['cart_id']
			print(self.context.user_id)
			(customer, created) = Customer.objects.get_or_create(user_id=self.context.user_id)
			order = Order.objects.create(customer=customer)
			cart_items = CartItem.objects.select_related('products').filter(cart_id=self.validated_data['cart_id'])
			order_items = [OrderItem(
				order=order,
				product=item.product,
				unit_price = item.product.unit_price,
				quantity=item.quantity
			) for item in cart_items]
			OrderItem.objects.bulk_create(order_items)
			Cart.objects.filter(pk=cart_id).delete()
			return order

class updateOrderSerialzer(serializers.ModelSerializer):
	class Meta:
		model = Order
		fields = ['payment_status']