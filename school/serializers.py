from rest_framework import serializers

from .models import School, Class, SpecialClass

class Get_School_Serializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ('id','school_code',"name",'customize')


class Get_Class_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'
        depth = 1
        
        

class Get_SpecialClass_Serializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialClass
        fields = '__all__'
        depth = 1
       