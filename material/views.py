from django.shortcuts import render
from .models import Video

# Create your views here.
def fileView(request):
    files = Video.objects.all()[0]
    return render(request,'material/home.html',{"files":files})
    