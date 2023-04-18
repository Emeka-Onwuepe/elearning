from user.serializers import Get_User_Serializer, User_Serializer, Login_Serializer
from django.contrib.auth import get_user_model
User=get_user_model()
from rest_framework import permissions,generics,status
from rest_framework.response import Response
from knox.models import AuthToken

class LoginUser(generics.GenericAPIView):
    serializer_class = Login_Serializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data['data'])
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        _, token = AuthToken.objects.create(user)
        returnedUser = Get_User_Serializer(user)
        #         content={"Access denied":"Access Denied, please request for access from the appropriate body"}
        #         return Response(content,status=status.HTTP_403_FORBIDDEN)
        return Response({"user": returnedUser.data, "token": token})

class RegisterUser(generics.GenericAPIView):
    serializer_class = User_Serializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        _,token=AuthToken.objects.create(user)
        returnedUser=Get_User_Serializer(user)
        return Response({"user":returnedUser.data,"token":token})