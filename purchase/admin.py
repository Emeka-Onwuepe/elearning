from django.contrib import admin

from purchase.models import Purchase

# Register your models here.
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ("buyer","total",'paid','date')

admin.site.register(Purchase,PurchaseAdmin)