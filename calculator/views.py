from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from bootstrap_modal_forms.generic import BSModalCreateView

from .models import *
from .forms import *


def Index(request):
    recipes = Recipe.objects.all()
    context = {'recipes': recipes}
    return render(request, 'index.html', context)


@login_required
def RecipeRecountView(request, pk):
    recipe = Recipe.objects.get(pk=pk)
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
    form_class = RecipeForm
    template_name = 'calculator/recipe_form.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        ingredients_form = IngredientsInlineFormset(instance=self.object)
        return self.render_to_response(self.get_context_data(form=form, ingredients_form=ingredients_form, edit=True))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        ingredients_form = IngredientsInlineFormset(self.request.POST, instance=self.object)
        if form.is_valid() and ingredients_form.is_valid():
            return self.form_valid(form, ingredients_form)
        else:
            return self.form_invalid(form, ingredients_form)

    def form_valid(self, form, ingredients_form):
        self.object = form.save(commit=False)
        self.object.save()
        recipe_metas = ingredients_form.save(commit=False)

        for obj in ingredients_form.deleted_objects:
            obj.delete()

        for meta in recipe_metas:
            meta.recipe = self.object
            meta.save()
        url = self.object.get_absolute_url()
        return redirect(url)

    def form_invalid(self, form, ingredients_form):
        return self.render_to_response(self.get_context_data(form=form, ingredients_form=ingredients_form))



class RecipeCreate(LoginRequiredMixin, generic.CreateView):
    form_class = RecipeForm
    template_name = 'calculator/recipe_form.html'

    def get_context_data(self, **kwargs):
        context = super(RecipeCreate, self).get_context_data(**kwargs)
        context['ingredients_form'] = IngredientsInlineFormset()
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        ingredients_form = IngredientsInlineFormset(self.request.POST)
        if form.is_valid() and ingredients_form.is_valid():
            return self.form_valid(form, ingredients_form)
        else:
            return self.form_invalid(form, ingredients_form)

    def form_valid(self, form, ingredients_form):
        self.object = form.save(commit=False)
        self.object.save()
        # saving ProductMeta Instances
        recipe_metas = ingredients_form.save(commit=False)
        for meta in recipe_metas:
            meta.recipe = self.object
            meta.save()
        url = self.object.get_absolute_url()
        return redirect(url)

    def form_invalid(self, form, ingredients_form):
        return self.render_to_response(self.get_context_data(form=form, ingredients_form=ingredients_form))


class ComponentCreate(LoginRequiredMixin, BSModalCreateView):
    form_class = ComponentForm
    template_name = 'calculator/component_form.html'
    model = Component
    success_message = 'Ингредиент создан'
    success_url = reverse_lazy('recipe_create')


class ComponentUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Component
    form_class = ComponentForm
