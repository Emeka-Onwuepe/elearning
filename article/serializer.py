from rest_framework import serializers

from .models import Article, Sections

class Get_Article_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
        depth = 1
        
 
class Get_Section_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Sections
        fields = '__all__'
        depth = 1   