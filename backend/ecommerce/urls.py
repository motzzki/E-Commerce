# ecommerce/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet

# Create a DefaultRouter to automatically generate API routes
router = DefaultRouter()
router.register(r'products', ProductViewSet)  # Register your ProductViewSet here

# Define your URL patterns
urlpatterns = [
    path('api/', include(router.urls)),  # API routes will be prefixed with "api/"
]
