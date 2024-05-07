from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from Main.models import *
from .models import *
from .serializers import *
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes 
from rest_framework.exceptions import ValidationError

class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        password = request.data.get('password')
        username = request.data.get('username')

        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)  
        except User.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        response_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'username': username,
            'userId': user.id,
            'is_superuser': user.is_superuser,  
        }
        
        return Response(response_data, status=status.HTTP_200_OK)


class AddToCartView(APIView):
    def post(self, request):
        product_id = request.data.get('product_id')  
        user_id = request.user.id  
        quantity = int(request.data.get('quantity', 1))

        product = get_object_or_404(Product, id=product_id)

        cart_item, created = CartItem.objects.get_or_create(user_id=user_id, product=product)

        if not created:
            return Response({"message": "Product already exists in the cart."}, status=status.HTTP_400_BAD_REQUEST)

        if quantity < 1:
            quantity = 1

        cart_item.quantity = quantity
        cart_item.save()

        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
class CartItemList(APIView):
    def get(self, request, user_id):
        cart_items = CartItem.objects.filter(user_id=user_id)
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data)
    


class UpdateCartView(APIView):
    def post(self, request):
        product_id = request.data.get('product_id')
        user_id = request.user.id 
        action = request.data.get('action')

        product = get_object_or_404(Product, id=product_id)

        cart_item, created = CartItem.objects.get_or_create(user_id=user_id, product=product)

        if action == 'increment':
            if product.quantity_available <= cart_item.quantity:
                raise ValidationError("Cannot increment quantity. Maximum quantity reached.")
            cart_item.quantity += 1
        elif action == 'decrement':
            if cart_item.quantity <= 1:
                raise ValidationError("Cannot decrement quantity. Minimum quantity reached.")
            cart_item.quantity -= 1

        cart_item.save()

        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class DeleteCartItemView(APIView):
    def post(self, request):
        product_id = request.data.get('product_id')  
        user_id = request.user.id  

        cart_item = get_object_or_404(CartItem, user_id=user_id, product_id=product_id)

        cart_item.delete()

        return Response({"message": "Cart item deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


from django.db import transaction

class CheckoutView(APIView):
    def post(self, request):
        cart_items = request.data.get('cart_items', [])
        total_price = 0
        order_items = []
        
        with transaction.atomic():
            order = Order.objects.create(user=request.user, total_price=0, status='Pending')
            for item in cart_items:
                product_id = item['product_id']
                quantity = item['quantity']
                price = calculate_price(product_id, quantity)
                total_price += price
                
                # Create order item
                order_item = OrderItem.objects.create(order=order, product_id=product_id, quantity=quantity, price_at_purchase=price)
                order_items.append(order_item)
                
                # Update product quantity available in the database
                product = Product.objects.get(pk=product_id)
                product.quantity_available -= quantity
                product.save()
            
            order.total_price = total_price
            order.save()
            
            # Delete cart items after successful checkout
            CartItem.objects.filter(product_id__in=[item['product_id'] for item in cart_items], user=request.user).delete()
        
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

def calculate_price(product_id, quantity):
    try:
        product = Product.objects.get(id=product_id)
        return product.price * quantity
    except Product.DoesNotExist:
        return 0 
    
    
    
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def user_orders(request):
#     orders = Order.objects.filter(user=request.user)
#     serializer = OrderSerializer(orders, many=True)
#     return Response(serializer.data)


@api_view(['GET'])
def user_orders(request):
    orders = Order.objects.all() 

    for order in orders:
        for order_item in order.order_items.all():
            product_id = order_item.product_id
            product = Product.objects.get(id=product_id)
            order_item.product_name = product.title  
            order_item.product_image = product.image.url 
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)