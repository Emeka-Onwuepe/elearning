from django.contrib import admin

from .models import School,Class,Set,Term,SpecialClass
from user.models import User
# Register your models here.

class SetAdmin(admin.ModelAdmin):
    list_display = ("name","school",'customize')
    filter_horizontal = ("students",)

    def formfield_for_manytomany(self,db_field,request,**kwargs):
        if db_field.name == "students":
            kwargs["queryset"] = User.objects.filter(user_type="student")
        return super(SetAdmin,self).formfield_for_manytomany(db_field,request,**kwargs)

class SchoolAdmin(admin.ModelAdmin):
    list_display = ("name","school_code",'customize')
    

admin.site.register(School,SchoolAdmin)
admin.site.register(Class)
admin.site.register(Set,SetAdmin)
admin.site.register(Term)
admin.site.register(SpecialClass)