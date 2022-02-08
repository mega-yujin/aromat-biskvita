from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.http import HttpResponse, Http404
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from bootstrap_modal_forms.generic import BSModalCreateView
from django.utils import timezone
import json

from .models import *
from .forms import *


class UpdatedLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data['remember_me']
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        return super(UpdatedLoginView, self).form_valid(form)


@login_required
def Index(request):
    owner = request.user
    recipes = Recipe.objects.filter(owner=owner).order_by('-recipestatistic__views')
    if recipes.exists():
        context = {'recipes': recipes}
    else:
        context = {'recipes': -1}
    return render(request, 'index.html', context)


@login_required
def RecipeRecountView(request, pk):
    recipe = Recipe.objects.get(pk=pk)
    user = request.user
    if recipe.owner == user:
        context = {'recipe': recipe}
        return render(request, 'calculator/recipe_recount.html', context)
    else:
        raise Http404("Такой страницы не существует или у Вас нет прав для её просмотра")


@login_required
def ShoppingListView(request):
    return render(request, 'calculator/shopping_list.html')


class RecipeListView(LoginRequiredMixin, generic.ListView):
    model = Recipe
    paginate_by = 12

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset().filter(owner=request.user)
        context = self.get_context_data()
        return self.render_to_response(context)


class RecipeDetailView(LoginRequiredMixin, generic.DetailView):
    model = Recipe

    # extra_context = {'form': Recipe.objects.get(pk=generic.DetailView.pk_url_kwarg)}

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        user = request.user
        if self.object.owner == user:
            counter, created = RecipeStatistic.objects.get_or_create(recipe=self.object)
            counter.views += 1
            counter.save()
            return self.render_to_response(self.get_context_data())
        else:
            raise Http404("Такой страницы не существует или у Вас нет прав для её просмотра")


class RecipeDelete(LoginRequiredMixin, generic.DeleteView):
    model = Recipe
    success_url = reverse_lazy('recipes')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        user = request.user
        if self.object.owner == user:
            return self.render_to_response(self.get_context_data())
        else:
            raise Http404("Такой страницы не существует или у Вас нет прав для её просмотра")


class RecipeUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'calculator/recipe_form.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        user = request.user
        if self.object.owner == user:
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            ingredients_form = IngredientsInlineFormset(instance=self.object)
            return self.render_to_response(
                self.get_context_data(form=form, ingredients_form=ingredients_form, edit=True))
        else:
            raise Http404("Такой страницы не существует или у Вас нет прав для её просмотра")

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
        user = request.user
        if form.is_valid() and ingredients_form.is_valid():
            return self.form_valid(form, ingredients_form, user)
        else:
            return self.form_invalid(form, ingredients_form)

    def form_valid(self, form, ingredients_form, user):
        self.object = form.save(commit=False)
        # saving user as recipe owner
        self.object.owner = user
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

# @login_required
# class FavoritesView(generic.View):
#     model = Favorites
#
#     def post(self, request, pk):
#         user = get_user(request)
#         # пытаемся получить закладку из таблицы, или создать новую
#         bookmark, created = self.model.objects.get_or_create(user=user, recipe_id=pk)
#         # если не была создана новая закладка,
#         # то считаем, что запрос был на удаление закладки
#         if not created:
#             bookmark.delete()
#
#         return HttpResponse(json.dumps({"result": created,
#                                         "count": self.model.objects.filter(recipe_id=pk).count()}),
#                             content_type="application/json")
