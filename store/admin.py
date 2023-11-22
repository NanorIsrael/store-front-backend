from django.contrib import admin
from . import models

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ['title', 'unit_price', 'inventory_status']
	list_editable = ['unit_price']
	list_per_page = 10

	@admin.display(ordering=['inventory'])
	def inventory_status(self, product):
		if product.inventory < 100:
			return 'Low'
		else:
			return 'Ok'
# Register your models here.
admin.site.register(models.Collection)
