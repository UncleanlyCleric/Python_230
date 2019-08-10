from django.contrib import admin
from blogging.models import Post, Category

'''
Creating ModelAdmin and CategoryInline for the PostAdmin page
'''
class CategoryInline(admin.TabularInline):
    model = Category.posts.through


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [
        CategoryInline,
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    '''
    Excluding posts
    '''
    exclude = ('posts',)
