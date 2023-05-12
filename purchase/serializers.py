from rest_framework import serializers

from purchase.models import Purchase


class Get_Purchase_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        exclude = ('buyer',)
        depth = 1