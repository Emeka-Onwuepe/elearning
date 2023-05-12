
from django.shortcuts import get_object_or_404

from school.models import School,Set,Class,SpecialClass
from school.serializers import (Get_School_Serializer,Get_Class_Serializer,
                                Get_SpecialClass_Serializer)

from rest_framework import permissions,generics
from rest_framework.response import Response

class GetSchoolData(generics.GenericAPIView):
  

    def get(self, request, *args, **kwargs):

        schoolId = request.query_params['id']
        # school = School.objects.get_or(school_code = schoolId)
        school = get_object_or_404(School,school_code = schoolId)

        if school.customize:
            classes = SpecialClass.objects.filter(set__school=school.id)
            class_data = Get_Class_Serializer(classes,many= True)
        else:
            classes = Class.objects.filter(set__school=school.id)
            class_data = Get_SpecialClass_Serializer(classes,many= True)
            
        serializer = Get_School_Serializer(school)
      
        return Response({"school": serializer.data,'classes':class_data.data})
        
        