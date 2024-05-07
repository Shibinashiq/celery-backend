from django.urls import path
from .views import *

urlpatterns = [
    path('addproducts/', ProductCreateAPIView.as_view(), name='product-create'),
    path('showproducts/', ProductListAPIView.as_view(), name='product-list'),
  # path('task/', test, name='task'), 
  path('test/', trigger_email_task.as_view(), name='test'), 

]