from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.Index, name='index'),
    path('recipes/', views.RecipeListView.as_view(), name='recipes'),
    path('shoppinglist/', views.ShoppingListView, name='shopping_list'),

    url(r'^recipe/(?P<pk>\d+)$', views.RecipeDetailView.as_view(), name='recipe-detail'),
    url(r'^recipe/(?P<pk>\d+)/delete/$', views.RecipeDelete.as_view(), name='recipe_delete'),
    url(r'^recipe/(?P<pk>\d+)/edit/$', views.RecipeUpdate.as_view(), name='recipe_update'),
    url(r'^recipe/(?P<pk>\d+)/recount/$', views.RecipeRecountView, name='recipe_recount'),
    url(r'^recipe/create/$', views.RecipeCreate.as_view(), name='recipe_create'),
    url(r'^component/create/$', views.ComponentCreate.as_view(), name='component_create'),
    url(r'^component/update/$', views.ComponentUpdate.as_view(), name='component_update'),
]
