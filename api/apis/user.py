from school.models import Set
from user.serializers import Get_User_Serializer, User_Serializer, Login_Serializer
from django.contrib.auth import get_user_model
from django.shortcuts import get_list_or_404

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
        data = request.data
        student_class_id = data.get('student_class')
        if student_class_id:
            if data['customize']:
                # student_set = get_list_or_404(Set,)
                student_set = Set.objects.filter(school=data['school_id'],special_class=student_class_id)
            else:
                student_set = Set.objects.filter(school=data['school_id'],set_class=student_class_id)
            if student_set:
                student_set[len(student_set)-1].students.add(user)
            else:
                raise 
        _,token=AuthToken.objects.create(user)
        returnedUser=Get_User_Serializer(user)
        return Response({"user":returnedUser.data,"token":token})