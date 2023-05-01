from rest_framework import routers
from django.urls import path
from knox import views as KnoxView

from .apis.course import Get_Course, Get_Courses, Get_Lession
router = routers.DefaultRouter()
from .apis.user import RegisterUser,LoginUser
from .apis.school import GetSchoolData


urlpatterns = [
    path('register', RegisterUser.as_view(), name="register"),
    path('login', LoginUser.as_view(), name="login"),
    path('getschool',GetSchoolData.as_view(),name='getshool'),
    path('logout', KnoxView.LogoutView.as_view(), name="knox_logout"),
    path('getcourses', Get_Courses.as_view(), name="get_courses"),
    path('getcourse', Get_Course.as_view(), name="get_courses"),
    path('getlesson', Get_Lession.as_view(), name="get_lesson"),
]

urlpatterns += router.urls