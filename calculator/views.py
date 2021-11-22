from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *


def Index(request):
    recipes = Recipe.objects.all()
    context = {'recipes': recipes}
    return render(request, 'index.html', context)


@login_required
def RecipeRecountView(request, pk):
    recipe = Recipe.objects.get(pk=pk)
    # form_choices = tuple()

    context = {'recipe': recipe}
    return render(request, 'calculator/recipe_recount.html', context)


class RecipeListView(LoginRequiredMixin, generic.ListView):
    model = Recipe
    paginate_by = 20


class RecipeDetailView(LoginRequiredMixin, generic.DetailView):
    model = Recipe
    # extra_context = {'form': Recipe.objects.get(pk=generic.DetailView.pk_url_kwarg)}


class RecipeDelete(LoginRequiredMixin, generic.DeleteView):
    model = Recipe
    success_url = reverse_lazy('recipes')


class RecipeUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Recipe
    # fields = '__all__'
    form_class = RecipeForm
    template_name = 'calculator/recipe_form.html'

    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     # context['recipe_meta_formset'] = IngredientsInlineFormset()
    #     context['recipe_meta_formset'] = object
    #     return context


class RecipeCreate(LoginRequiredMixin, generic.CreateView):
    form_class = RecipeForm
    template_name = 'calculator/recipe_form.html'

    def get_context_data(self, **kwargs):
        context = super(RecipeCreate, self).get_context_data(**kwargs)
        context['ingredients'] = IngredientsInlineFormset()
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        ingredients = IngredientsInlineFormset(self.request.POST)
        if form.is_valid() and ingredients.is_valid():
            return self.form_valid(form, ingredients)
        else:
            return self.form_invalid(form, ingredients)

    def form_valid(self, form, ingredients):
        self.object = form.save(commit=False)
        self.object.save()
        # saving ProductMeta Instances
        recipe_metas = ingredients.save(commit=False)
        print(recipe_metas)
        for meta in recipe_metas:
            meta.recipe = self.object
            meta.save()
        url = self.object.get_absolute_url()
        return redirect(url)

    def form_invalid(self, form, ingredients):
        return self.render_to_response(self.get_context_data(form=form, ingredients=ingredients))


class ComponentCreate(LoginRequiredMixin, generic.CreateView):
    model = Component
    form_class = ComponentForm


class ComponentUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Component
    form_class = ComponentForm
