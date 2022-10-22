from django.contrib import admin

# Register your models here.
from mptt.admin import MPTTModelAdmin
from .models import Category,Product


# class Categorylist(admin.ModelAdmin):
#     list_display = ('name','image_tag')
# admin.site.register(Category,Categorylist)

admin.site.register(Category , MPTTModelAdmin ) 
admin.site.register(Product) 