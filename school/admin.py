from django.contrib import admin

from .models import School,Class,Set,Term,SpecialClass
from user.models import User
# Register your models here.

class SetAdmin(admin.ModelAdmin):
    list_display = ("name","school",'special_class','set_class','customize')
    filter_horizontal = ("students",)
    actions = ["update_class"]

    @admin.action(description="Update Class")
    def update_class(self, request, queryset):
        for query in queryset:
            if query.customize:
                prefix,level,num = None,None,0
                try:
                    prefix,level,num = query.special_class.name.split('_')
                except Exception:
                    pass
                
                
                if level == 'kg' and num !=0:
                    if num == '2':
                        new_class, Created = SpecialClass.objects.get_or_create(name=f'{prefix}_primary_1')
                        query.special_class = new_class
                        query.save()
                    else:
                        new_class, Created = SpecialClass.objects.get_or_create(name=f'{prefix}_{level}_2')
                        query.special_class = new_class
                        query.save()
                elif level == 'primary'and num !=0:
                    num = int(num)
                    if num < 6:
                        new_class, Created = SpecialClass.objects.get_or_create(name=f'{prefix}_{level}_{num+1}')
                        query.special_class = new_class
                        query.save()
                    else:
                        query.special_class = None
                        query.save()
                     
            else:
                level,num = None,0
                try:
                    level,num = query.set_class.name.split('_')
                except Exception:
                    pass
                
                if level == 'kg' and num !=0:
                    if num == '2':
                        new_class, Created = Class.objects.get_or_create(name='primary_1')
                        query.set_class = new_class
                        query.save()
                    else:
                        new_class, Created = Class.objects.get_or_create(name=f'{level}_2')
                        query.set_class = new_class
                        query.save()
                elif level == 'primary' and num !=0:
                    num = int(num)
                    if num < 6:
                        new_class, Created = Class.objects.get_or_create(name=f'{level}_{num+1}')
                        query.set_class = new_class
                        query.save()
                    else:
                         query.set_class = None
                         query.save()
                     
                
                 

    def formfield_for_manytomany(self,db_field,request,**kwargs):
        if db_field.name == "students":
            kwargs["queryset"] = User.objects.filter(user_type="student")
        return super(SetAdmin,self).formfield_for_manytomany(db_field,request,**kwargs)

class SchoolAdmin(admin.ModelAdmin):
    list_display = ("name","school_code",'customize')

class ClassAdmin(admin.ModelAdmin):
    list_display = ("name","term")
    actions = ["update_term"]

    @admin.action(description="Update Term")
    def update_term(self, request, queryset):
        limit = 3
        current = queryset[0].term
        figure = current+1 if current < 3 else 1
        queryset.update(term=figure) 

admin.site.register(School,SchoolAdmin)
admin.site.register(Class,ClassAdmin)
admin.site.register(Set,SetAdmin)
admin.site.register(Term)
admin.site.register(SpecialClass,ClassAdmin)