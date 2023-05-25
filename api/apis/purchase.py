import requests
from rest_framework import permissions,generics
from rest_framework.response import Response
from course.models import Course, Course_set

from purchase.models import Purchase
from elearning import settings
from purchase.serializers import Get_Purchase_Serializer
# from django.shortcuts import 


class ProcessPurchase(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        
        if data['action'] == "create":
            purchase, created = Purchase.objects.get_or_create(buyer=user, total=data['total'],
                                                               purchase_id = data['purchase_id'])
            if created:
                for item in data['items']:
                    if item['type'] == 'course':
                        course = Course.objects.get(pk=item['id'])
                        course.purchase_count += 1
                        course.save()
                        purchase.courses.add(course)
                    else:
                        print(item['id'])
                        ids = Course_set.objects.all().values('id')
                        course_set = Course_set.objects.get(pk=item['id'])
                        course_set.purchase_count += 1
                        course_set.save()
                        purchase.course_sets.add(course_set)
            return Response({'created':created,'id':purchase.id})    
        
        if data['action'] == "confirm":
            
            headers = {
                    "Authorization": f'Bearer {settings.PAYSTACT_SECRET_KEY}',
                        'Content-Type': 'application/json',
                }
            url = f'https://api.paystack.co/transaction/verify/{data["purchase_id"]}'
                
            response = requests.get(url,headers=headers)
                
            if response.status_code == 200:
                #    response_data = response.json()
                purchase = Purchase.objects.get(purchase_id = data['purchase_id'])
                purchase.paid = True
                purchase.save()
                
                return Response({"success":True})
           
            
        return Response({})
    
class GetPurchases(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        
        purchases = Purchase.objects.filter(buyer=request.user.id)
        data = Get_Purchase_Serializer(purchases,many=True).data
        
        return Response(data)
    
    
class DeletePurchase(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        id = request.data
        purchase = Purchase.objects.get(id =int(id))
        purchase.delete()
        # purchases = Purchase.objects.filter(buyer=request.user.id)
        # data = Get_Purchase_Serializer(purchases,many=True).data
        return Response({"resolved":True})
        
    
    