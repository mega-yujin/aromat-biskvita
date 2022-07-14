from django.contrib import admin
from .models import Recipe, Ingredients, Component, RecipeStatistic


class RecipesInline(admin.TabularInline):
    model = Ingredients
    extra = 1
    autocomplete_fields = ('recipe', 'component')


@admin.register(Recipe)
class RecipesAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'weight', 'form', 'diameter', 'length', 'width', 'height', 'owner')
    ordering = ['name']
    search_fields = ['name', 'description']
    list_per_page = 50

    inlines = [RecipesInline]


@admin.register(Component)
class ComponentsAdmin(admin.ModelAdmin):
    list_display = ('name', 'units')
    list_editable = ('units',)
    ordering = ['name']
    search_fields = ['name']
    list_per_page = 50


@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'recipe', 'component', 'quantity', 'units', 'annotation')
    list_display_links = ('name',)
    list_editable = ('recipe', 'component', 'quantity', 'annotation')
    ordering = ['recipe', 'component']
    list_per_page = 50
    autocomplete_fields = ('recipe', 'component')

    def units(self, record):
        return record.component.units


@admin.register(RecipeStatistic)
class RecipesStatisticAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'views')
    search_fields = ('__str__',)
