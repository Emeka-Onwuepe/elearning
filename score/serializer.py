from rest_framework import serializers

from score.models import Course_Score, Quiz_Score


class Get_Course_Score_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Course_Score
        fields = '__all__'
        
class Get_Quiz_Score_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz_Score
        fields = '__all__'