# ecommerce/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, RegisterView, LoginView, UserProfileView, OrderViewSet

# Create a DefaultRouter to automatically generate API routes
router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')  # Register your ProductViewSet here
router.register(r'orders', OrderViewSet, basename='order')
# Define your URL patterns
urlpatterns = [
    path('api/', include(router.urls)),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/users/', UserProfileView.as_view(), name='user-profile'),

]
