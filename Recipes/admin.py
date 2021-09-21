from django.contrib import admin
from .models import Author, Recipe

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'bio')


class RecipeAdmin(admin.ModelAdmin):
    exclude = ('date_created', )
    list_display = ('title', 'description', 'required_time', 'instructions')


admin.site.register(Author, AuthorAdmin)
admin.site.register(Recipe, RecipeAdmin)