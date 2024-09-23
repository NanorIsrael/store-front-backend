from django.urls import include, path
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
# router.register('products', views.ProductViewSet)

products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet, basename='reviews')
urlpatterns = [
	path('', include(router.urls)),
	path(r'', include(products_router.urls))
]