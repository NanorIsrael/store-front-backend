from django.shortcuts import render
from django.http import HttpResponse
from store.models import Order, OrderItem, Collection, Product, Customer
from django.db.models.aggregates import Count, Sum, Min, Max, Avg


# Create your views here.
def say_hello(request):
	# how many orders exist
	query_set = Order.objects.aggregate(count=Count('id'))
	# how many of product 1 has been placed
	result2 = OrderItem.objects.filter(product__id=1).aggregate(quantity_sold=Sum('quantity'))
	# how many orders belong to customer 1
	result3 = Order.objects.filter(customer__id=1).aggregate(quantity_placed=Count('id'))\

	result4 = Product.objects.filter(collection__id=3).aggregate(
		min=Min('unit_price'),
		max=Max('unit_price'),
		average=Avg('unit_price')
	)


	print(query_set)
	print(result2)
	print(result3)
	print(result4)

	result5 =  Customer.objects.filter(email__icontains='.com')
	result6 =  Collection.objects.filter(featured_product__isnull=True)
	print(result5)
	print(result6)

	return render(request, 'hello.html')