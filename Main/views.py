from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product
from .serializers import *
from rest_framework.generics import ListAPIView
class ProductCreateAPIView(APIView):
    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
from django.http import HttpResponse
from .task import test_func 
    
def test (request):
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    test_func.delay()
    return HttpResponse("Done")