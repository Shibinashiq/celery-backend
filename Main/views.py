from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product
from .serializers import *
from rest_framework.generics import ListAPIView
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http import HttpResponse


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
    

    
# def test (request):
#     print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
#     test_func.delay()
#     return HttpResponse("Done")


from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .task import celery_task

# @login_required
class trigger_email_task(APIView):
    def post(self,request):
        print(request.user.email)
        celery_task.delay(request.user.email)
        return JsonResponse({'status': 'success'})
       