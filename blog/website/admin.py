from django.contrib import admin
from .models import Blog 
# Register your models here.



@admin.register(Blog)

class BlogAdmin(admin.ModelAdmin):
  search_fields=Blog.SearchableFields
  list_filter = Blog.FilterFields