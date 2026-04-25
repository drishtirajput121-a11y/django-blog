from django.contrib import admin
from .models import Category , Blog

class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'category', 'author', 'status', 'is_featured', 'created_at')
    search_fields = ('title', 'category__category_name','status', 'id')
    list_editable = ('is_featured',)
admin.site.register(Category)
# Register your models here.
admin.site.register(Blog, BlogAdmin)