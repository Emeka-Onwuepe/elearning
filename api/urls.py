from rest_framework import routers
from django.urls import path
from knox import views as KnoxView

from api.apis.purchase import GetPurchases, ProcessPurchase,DeletePurchase
from api.apis.quiz import Get_Quiz_Score,Get_Course_Score, Quiz_View

from .apis.course import (Get_Course, Get_Courses,Get_Category, 
                          Get_Material,
                          Get_Sections,Get_Article,)
router = routers.DefaultRouter()
from .apis.user import RegisterUser,LoginUser, SetUser
from .apis.school import GetSchoolData


urlpatterns = [
    path('register', RegisterUser.as_view(), name="register"),
    path('login', LoginUser.as_view(), name="login"),
    path('getschool',GetSchoolData.as_view(),name='getshool'),
    path('logout', KnoxView.LogoutView.as_view(), name="knox_logout"),
    path('getcourses', Get_Courses.as_view(), name="get_courses"),
    path('getcourse', Get_Course.as_view(), name="get_courses"),
    path('getmaterial', Get_Material.as_view(), name="get_material"),
    path('setuser', SetUser.as_view(), name="set_user"),
    path('processpurchase', ProcessPurchase.as_view(), name="process_purchase"),
    path('getpurchases',GetPurchases.as_view(),name="get_purchases"),
    path('deletepurchase',DeletePurchase.as_view(),name="delete_purchases"),
    path('getcategory',Get_Category.as_view(),name="get_category"),
    path('getarticle',Get_Article.as_view(),name="get_article"),
    path('getsection',Get_Sections.as_view(),name="get_section"),
    path('quizview',Quiz_View.as_view(),name="quiz_view"),
    path('getquizscore',Get_Quiz_Score.as_view(),name="get_quiz_score"),
    path('getcoursescore',Get_Course_Score.as_view(),name="get_course_score"),
           
]

urlpatterns += router.urls