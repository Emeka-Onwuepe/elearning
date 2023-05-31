from django.utils.html import format_html
from django.contrib import admin
from .models import Article, Sections
from elearning.settings import CORS_ORIGIN_WHITELIST
# Register your models here.

admin.site.register(Sections)

class Inline_Sections(admin.StackedInline):
    model = Sections
    extra = 1

class Article_Admin(admin.ModelAdmin):
    inlines = [Inline_Sections]
    
    def view_article(self):
        link = f'{CORS_ORIGIN_WHITELIST[0]}/admin/article/{self.id}'
        return format_html(f'<a target="_blank" href="{link}">view</a>')
    
    list_display = ['title','pub_date','mod_date',view_article]
    
  
    
    
admin.site.register(Article,Article_Admin)