from django.contrib import admin
from .models import Video,Material


class MaterialAdmin(admin.ModelAdmin):
    list_display = ("material_type","video",'article','quiz')
    
    

# Register your models here.
admin.site.register(Video)
admin.site.register(Material,MaterialAdmin)
