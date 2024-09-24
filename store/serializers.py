from decimal import Decimal
from rest_framework import serializers
from .models import Product, Collection, Reviews, Cart, CartItem

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
	total_price = serializers.SerializerMethodField(method_name='totol_price')
	
	def total_price(self, cart_item: CartItem):
		return cart_item.quantity * cart_item.product.unit_price

	class Meta:
		model = CartItem
		fields = ['id', 'product', 'quantity', 'cart', 'total_price']


class CartSerializer(serializers.ModelSerializer):
	id = serializers.UUIDField(read_only=True)
	items = CartItemSerializer(many=True)
	class Meta:
		model = Cart
		fields = ['id', 'created_at', 'items']

class AddCartItemSerializer(serializers.ModelSerializer):
	class Meta:
		model = CartItem
		fields = ['id', 'product_id', 'quantity']