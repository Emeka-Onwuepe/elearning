from rest_framework import routers
from django.urls import path
from knox import views as KnoxView
router = routers.DefaultRouter()
from .apis.user import RegisterUser,LoginUser


urlpatterns = [
    path('register', RegisterUser.as_view(), name="register"),
    path('login', LoginUser.as_view(), name="login"),
    path('logout', KnoxView.LogoutView.as_view(), name="knox_logout"),
]

urlpatterns += router.urls