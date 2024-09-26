from django.urls import include, path
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('cart', views.CartViewSet, basename="cart")
router.register('cart-items', views.CartItemViewSet, basename="cart-item")
router.register('collections', views.CollectionViewSet, basename="collections")

# router.register('products', views.ProductViewSet)

products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
cart_router = routers.NestedDefaultRouter(router, 'cart', lookup='cart')
cart_router.register('items', views.CartItemViewSet, basename="item")

products_router.register('reviews', views.ReviewViewSet, basename='reviews')
urlpatterns = [
	path('', include(router.urls)),
	path(r'', include(cart_router.urls)),
	path(r'', include(products_router.urls)),
]