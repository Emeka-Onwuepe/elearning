from rest_framework import serializers

from quiz.models import Quiz

class Get_Quiz_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'
        depth = 3