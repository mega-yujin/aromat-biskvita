from django import forms
from django.forms import inlineformset_factory
from .models import Recipe, Ingredients, Component


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        # fields = '__all__'
        # fields = ('name', 'description', 'weight', 'form', 'diameter', 'length', 'width')
        exclude = ('components',)


class IngredientsForm(forms.ModelForm):
    class Meta:
        model = Ingredients
        # fields = ('quantity',)
        fields = '__all__'


class ComponentForm(forms.ModelForm):
    class Meta:
        model = Component
        fields = '__all__'


IngredientsInlineFormset = inlineformset_factory(Recipe, Ingredients, form=IngredientsForm, extra=20)

# component = models.ForeignKey(Component, on_delete=models.CASCADE, verbose_name='Ингредиент')
#     recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='Рецепт')
#     quantity = models.FloatField(null=False, default=1, verbose_name='Количество')
