from django.contrib import admin
from . import models

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ['title', 'unit_price', 'inventory_status', 'collection_title']
	list_editable = ['unit_price']
	list_per_page = 10
	list_select_related = ['collection']

	@admin.display(ordering=['inventory'])
	def inventory_status(self, product):
		if product.inventory < 100:
			return 'Low'
		else:
			return 'Ok'
	def collection_title(self, product):
		return product.collection.title

# Register your models here.
admin.site.register(models.Collection)
