from django.apps import apps
from django.contrib import admin

from .models import Recipe

class RecipeProductInline(admin.TabularInline):
    model = Recipe.products.through
    extra = 1

class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeProductInline,)

admin.site.register(Recipe, RecipeAdmin)

app_config = apps.get_app_config('scheduler')
models = app_config.get_models()
for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
