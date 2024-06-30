from django.contrib import admin
from .models import Blog, Author
# Register your models here.


admin.site.register(Author)
@admin.register(Blog)
# Admin Fields

class BlogAdmin(admin.ModelAdmin):
  search_fields=Blog.SearchableFields
  list_filter = Blog.FilterFields