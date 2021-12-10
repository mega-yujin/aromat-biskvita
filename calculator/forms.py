from django import forms
from django.forms import inlineformset_factory
from bootstrap_modal_forms.forms import BSModalModelForm
from .models import Recipe, Ingredients, Component


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        # fields = '__all__'
        # fields = ('name', 'description', 'instruction', 'weight', 'form', 'diameter', 'length', 'width')
        exclude = ('components', 'owner', )

    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        for field, val in self.fields.items():
            val.widget.attrs['class'] = 'form-control mb-2 mr-sm-2'


class IngredientsForm(forms.ModelForm):
    class Meta:
        model = Ingredients
        # fields = ('quantity',)
        fields = '__all__'


class ComponentForm(BSModalModelForm):
    class Meta:
        model = Component
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ComponentForm, self).__init__(*args, **kwargs)
        for field, val in self.fields.items():
            val.widget.attrs['class'] = 'form-control'


IngredientsInlineFormset = inlineformset_factory(Recipe, Ingredients, form=IngredientsForm, extra=3)
