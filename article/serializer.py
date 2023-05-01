from rest_framework import serializers

from .models import Article

class Get_Article_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
        depth = 2