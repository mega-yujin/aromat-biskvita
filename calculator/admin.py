from django.contrib import admin
from .models import *


class RecipesInline(admin.TabularInline):
    model = Ingredients
    # fields = ('name', 'quantity', 'annotation')
    extra = 1
    autocomplete_fields = ('recipe', 'component')


class RecipesAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'weight', 'form', 'diameter', 'length', 'width', 'owner')
    ordering = ['name']
    search_fields = ['name', 'description']
    list_per_page = 50

    # fields = ('name', 'description', 'diameter', 'weight')
    inlines = [RecipesInline]


class ComponentsAdmin(admin.ModelAdmin):
    list_display = ('name', 'units')
    list_editable = ('units',)
    ordering = ['name']
    search_fields = ['name']
    list_per_page = 50


class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'recipe', 'component', 'quantity', 'units', 'annotation')
    list_display_links = ('name',)
    list_editable = ('recipe', 'component', 'quantity', 'annotation')
    ordering = ['recipe', 'component']
    list_per_page = 50
    autocomplete_fields = ('recipe', 'component')

    # search_fields = ('recipe',) # не работает

    def units(self, record):
        return record.component.units


class RecipesStatisticAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'views')
    search_fields = ('__str__', )


admin.site.register(Component, ComponentsAdmin)
admin.site.register(Ingredients, IngredientsAdmin)
admin.site.register(Recipe, RecipesAdmin)
admin.site.register(RecipeStatistic, RecipesStatisticAdmin)
