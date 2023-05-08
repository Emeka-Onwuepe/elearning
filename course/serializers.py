from rest_framework import serializers

from .models import Course,Course_set,Course_set_unit,Course_Unit,Course_Week,Category

class Get_Course_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
        depth = 1

class Get_Course_Set_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Course_set
        fields = '__all__'
        depth = 1

class Get_Course_Set_Unit_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Course_set_unit
        fields = '__all__'
        depth = 1

class Get_Course_Unit_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Course_Unit
        fields = '__all__'
        depth = 1
        
class Get_Course_Week_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Course_Week
        fields = '__all__'
        depth = 1

class Get_Category(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        