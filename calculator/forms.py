from django import forms
from django.forms import inlineformset_factory
from .models import Recipe, Ingredients, Component


class RecipeForm(forms.ModelForm):
    # name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Название')
    # description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', "rows": 5}), label='Описание')
    # instruction = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), label='Рецепт')
    # form = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), label='Форма', choices=Recipe.FORMS)
    # diameter = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}), label='Диаметр')
    # length = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}), label='Длина')
    # width = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}), label='Ширина')
    # weight = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}), label='Вес')

    class Meta:
        model = Recipe
        # fields = '__all__'
        # fields = ('name', 'description', 'instruction', 'weight', 'form', 'diameter', 'length', 'width')
        exclude = ('components',)

    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        for field, val in self.fields.items():
            val.widget.attrs['class'] = 'form-control mb-2 mr-sm-2'


class IngredientsForm(forms.ModelForm):
    class Meta:
        model = Ingredients
        # fields = ('quantity',)
        fields = '__all__'


class ComponentForm(forms.ModelForm):
    class Meta:
        model = Component
        fields = '__all__'


IngredientsInlineFormset = inlineformset_factory(Recipe, Ingredients, form=IngredientsForm, extra=5, can_delete=True)

# component = models.ForeignKey(Component, on_delete=models.CASCADE, verbose_name='Ингредиент')
#     recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='Рецепт')
#     quantity = models.FloatField(null=False, default=1, verbose_name='Количество')
