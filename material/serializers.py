from rest_framework import serializers

from .models import Material, Video

class Get_Material_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'
        depth = 1

class Get_Video_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'
        depth = 1
        
       