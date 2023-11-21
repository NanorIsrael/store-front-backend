from django.db import models

# Create your models here.``
class Promotion(models.Model):
	descriptions = models.CharField(max_length=255)
	disscount = models.FloatField()
	featured_product = models.ForeignKey('Product', on_delete=models.CASCADE)

class Collection(models.Model):
	title = models.CharField(max_length=255)
	featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')


class Product(models.Model):
	title = models.CharField(max_length=255)
	slug = models.SlugField(null=True)
	descriptions = models.TextField()
	price = models.DecimalField(max_digits=6,  decimal_places=2)
	inventory = models.IntegerField() 
	last_update = models.DateTimeField(auto_now=True)
	collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
	promotions = models.ManyToManyField(Promotion)

class Customer(models.Model):
	MEMBERSHIP_BRONZE = 'B'
	MEMBERSHIP_SILVER = 'S'
	MEMBERSHIP_GOLD = 'G'

	MEMBERSHIP_CHOICES = [
		(MEMBERSHIP_BRONZE, 'Bronze'),
		(MEMBERSHIP_SILVER, 'Silver'),
		(MEMBERSHIP_GOLD, 'Gold')
	]
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.EmailField(unique=True)
	phone = models.CharField(max_length=20)
	birth_date = models.DateTimeField(null=True)
	membership_type = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)


class Order(models.Model):

	PAYMENT_CHOICES = [
		('P', 'Pending'),
		('C', 'Complete'),
		('F', 'Failed')
	]
	place_at = models.DateTimeField(auto_now_add=True)
	membership_type = models.CharField(max_length=1, choices=PAYMENT_CHOICES, default='P')
	customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


class OrderItem(models.Model):
	Order = models.ForeignKey(Order, on_delete=models.PROTECT)
	product = models.ForeignKey(Product, on_delete=models.PROTECT)
	quatity = models.PositiveSmallIntegerField()
	unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Address(models.Model):
	street = models.CharField(max_length=255)
	city = models.CharField(max_length=255)
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE)


class Cart(models.Model):
	Create_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
	quatity = models.PositiveSmallIntegerField()
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
