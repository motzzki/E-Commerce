# serializers.py
from django.db import transaction
from rest_framework import serializers
from .models import Product, CustomUser, Order, OrderItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'user_type']  

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        user.user_type = validated_data['user_type'] 
        user.save()
        return user
    

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    
    class Meta:
        model = OrderItem
        fields = '__all__'
        
class OrderItemWriteSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(source='orderitem_set', many=True, read_only=True)
    write_items = OrderItemWriteSerializer(many=True, write_only=True)
    customer = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'created_at', 'items', 'write_items']

    def create(self, validated_data):
        items_data = validated_data.pop('write_items')

        with transaction.atomic():
            order = Order.objects.create(**validated_data)

            for item_data in items_data:
                product = item_data['product']
                quantity = item_data['quantity']

                if product.stock < quantity:
                    raise serializers.ValidationError(f"Not enough stock for '{product.name}'")

                product.stock -= quantity
                product.save()

                OrderItem.objects.create(order=order, product=product, quantity=quantity)

        return order



    
    
