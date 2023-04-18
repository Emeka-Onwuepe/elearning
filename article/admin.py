from django.contrib import admin
from .models import Article, Sections

# Register your models here.

admin.site.register(Sections)

class Inline_Sections(admin.StackedInline):
    model = Sections
    extra = 1

class Article_Admin(admin.ModelAdmin):
    inlines = [Inline_Sections]
    
admin.site.register(Article,Article_Admin)