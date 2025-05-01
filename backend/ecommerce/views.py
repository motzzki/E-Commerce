from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render
from .serializers import ProductSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Product, OrderItem

# Create your views here.
@login_required
def manage_products(request):
    if request.user.user_type != 'employee':
        return HttpResponseForbidden("Only employees can manage products.")
    return render(request, 'products/manage.html')

@login_required
def store_view(request):
    if request.user.user_type != 'customer':
        return HttpResponseForbidden("Only customers can access the store.")
    return render(request, 'store/storefront.html')


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        if OrderItem.objects.filter(product=product).exists():
            return Response(
                {"error": "Cannot delete product. It is part of an existing order."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)


