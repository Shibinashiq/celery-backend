from django.urls import path
from .views import *

urlpatterns = [
    path('addproducts/', ProductCreateAPIView.as_view(), name='product-create'),
    path('showproducts/', ProductListAPIView.as_view(), name='product-list'),
  path('task/', test, name='test'), 

]