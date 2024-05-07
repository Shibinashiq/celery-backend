from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *

urlpatterns = [
    
    
    path('signup/', SignupView.as_view(), name='user-signup'),
    path('login/', LoginView.as_view(), name='user-login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    
    
    
    
    path('add-to-cart/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart-items/<int:user_id>/', CartItemList.as_view(), name='cart_item_list'),
    path('update-cart/', UpdateCartView.as_view(), name='update_cart'),
    path('delete-cart-item/', DeleteCartItemView.as_view(), name='delete_cart_item'),
    
    
    
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('orders/', user_orders, name='user_orders'),
]
