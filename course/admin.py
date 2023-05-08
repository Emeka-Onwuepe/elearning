from django.contrib import admin
from .models import (Category, Course,Course_set,Course_set_unit,
                     Course_Unit,Course_Week)

# Register your models here.
admin.site.register(Course_set)
admin.site.register(Course_set_unit)
admin.site.register(Course)
admin.site.register(Course_Week)
admin.site.register(Course_Unit)
admin.site.register(Category)
