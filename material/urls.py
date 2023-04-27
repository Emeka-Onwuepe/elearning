from rest_framework import routers
from django.urls import path
from .import views
router = routers.DefaultRouter()


app_name="frontview"

urlpatterns = [
    
    path('',views.fileView,name="fileView"), 
    
    
   
      

]
urlpatterns += router.urls