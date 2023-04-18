from django.contrib import admin

from .models import School,Class,Set,Term
# Register your models here.

admin.site.register(School)
admin.site.register(Class)
admin.site.register(Set)
admin.site.register(Term)