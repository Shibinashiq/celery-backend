from rest_framework import serializers
from django.contrib.auth.models import User

from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
class CartItemSerializer(serializers.ModelSerializer):
    product_image = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'product_image', 'price', 'product_name']  

    def get_product_image(self, obj):
        return obj.product.image.url  

    def get_price(self, obj):
        return obj.product.price  

    def get_product_name(self, obj):
        return obj.product.title
    
    
    
    
    
class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.title', read_only=True)
    product_image = serializers.ImageField(source='product.image', read_only=True)  

    class Meta:
        model = OrderItem
        fields = ['product_name', 'quantity', 'price_at_purchase', 'product_image']
        
class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    user_total_orders = serializers.SerializerMethodField()

    def get_user_total_orders(self, obj):
        return Order.objects.filter(user=obj.user).count()

    class Meta:
        model = Order
        fields = ['id', 'user', 'user_username', 'user_total_orders', 'total_price', 'status', 'created_at', 'order_items']
        read_only_fields = ['id', 'user', 'total_price', 'status', 'created_at', 'order_items', 'user_username', 'user_total_orders']
