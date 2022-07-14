from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Component(models.Model):
    class Meta:
        verbose_name_plural = 'Компоненты'

    name = models.CharField(max_length=255, verbose_name='Название')
    units = models.CharField(max_length=50, verbose_name='Единица измрения')

    def __str__(self):
        return f"{self.name} ({self.units})"


class Recipe(models.Model):
    class Meta:
        verbose_name_plural = 'Рецепты'

    owner = models.ForeignKey(User, verbose_name='Создатель рецепта', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(null=True, verbose_name='Описание')
    instruction = models.TextField(null=True, blank=False, verbose_name='Рецепт приготовления')
    weight = models.FloatField(null=True, blank=False, verbose_name='Вес')
    FORMS = (
        ('c', 'Круглая'),
        ('s', 'Квадратная'),
        ('r', 'Прямоугольная'),
    )
    form = models.CharField(max_length=1, choices=FORMS, default='r', verbose_name='Форма')
    diameter = models.PositiveIntegerField(null=True, blank=True, verbose_name='Диаметр')
    length = models.PositiveIntegerField(null=True, blank=True, verbose_name='Длина')
    width = models.PositiveIntegerField(null=True, blank=True, verbose_name='Ширина')
    height = models.FloatField(null=True, blank=True, verbose_name='Высота')
    components = models.ManyToManyField(Component, through='Ingredients', through_fields=('recipe', 'component'),
                                        verbose_name='Ингредиенты')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('recipe-detail', args=[str(self.id)])

    def get_delete_url(self):
        return reverse('recipe_delete', args=[str(self.id)])

    def get_edit_url(self):
        return reverse('recipe_update', args=[str(self.id)])

    def get_recount_url(self):
        return reverse('recipe_recount', args=[str(self.id)])


class Ingredients(models.Model):
    class Meta:
        verbose_name_plural = 'Ингредиенты'
        unique_together = (('recipe', 'component', 'annotation'),)

    component = models.ForeignKey(Component, on_delete=models.CASCADE, verbose_name='Ингредиент')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='Рецепт')
    quantity = models.FloatField(null=False, default=1, verbose_name='Количество')
    annotation = models.CharField(max_length=255, null=True, blank=True, verbose_name='Примечание')

    def name(self):
        return self.recipe.name + "(%s)" % self.component.name


class RecipeStatistic(models.Model):
    class Meta:
        verbose_name_plural = 'Статистика просмотров'

    recipe = models.OneToOneField(Recipe, on_delete=models.CASCADE)
    views = models.IntegerField(verbose_name='Просмотры', default=0)

    def __str__(self):
        return self.recipe.name
