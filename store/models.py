from django.conf import settings
from django.db import models
from uuid import uuid4


# Create your models here.``
class Promotion(models.Model):
	descriptions = models.CharField(max_length=255)
	disscount = models.FloatField()
	featured_product = models.ForeignKey('Product', on_delete=models.CASCADE)

class Collection(models.Model):
	title = models.CharField(max_length=255)
	# featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')

	def __str__(self):
		return self.title
	
	class Meta:
		ordering = ['title']

class Product(models.Model):
	title = models.CharField(max_length=255)
	# slug = models.SlugField(null=True)
	description = models.TextField()
	unit_price = models.DecimalField(max_digits=6,  decimal_places=2)
	inventory = models.IntegerField() 
	last_update = models.DateTimeField(auto_now=True)
	collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
	# promotions = models.ManyToManyField(Promotion)

	def __str__(self):
		return self.title
	
	class Meta:
		ordering = ['title']

class Customer(models.Model):
	MEMBERSHIP_BRONZE = 'B'
	MEMBERSHIP_SILVER = 'S'
	MEMBERSHIP_GOLD = 'G'

	MEMBERSHIP_CHOICES = [
		(MEMBERSHIP_BRONZE, 'Bronze'),
		(MEMBERSHIP_SILVER, 'Silver'),
		(MEMBERSHIP_GOLD, 'Gold')
	]

	phone = models.CharField(max_length=20, blank=True)
	birth_date = models.DateTimeField(null=True)
	membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	def __str__(self) -> str:
		return f'{self.user.first_name} {self.user.last_name}'

	def first_name(self):
		return self.user.first_name

class Order(models.Model):

	PAYMENT_CHOICES = [
		('P', 'Pending'),
		('C', 'Complete'),
		('F', 'Failed')
	]
	placed_at = models.DateTimeField(auto_now_add=True)
	payment_status = models.CharField(max_length=1, choices=PAYMENT_CHOICES, default='P')
	customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


class OrderItem(models.Model):
	order = models.ForeignKey(Order, on_delete=models.PROTECT)
	product = models.ForeignKey(Product, on_delete=models.PROTECT)
	quantity = models.PositiveSmallIntegerField()
	unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Address(models.Model):
	street = models.CharField(max_length=255)
	city = models.CharField(max_length=255)
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE)


class Cart(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid4)
	created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
	quantity = models.PositiveSmallIntegerField()
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_item')

	class Meta:
		unique_together = [['cart', 'product']]

class Reviews(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
	name = models.CharField(max_length=255)
	description = models.TextField()
	date = models.DateField(auto_now_add=True)