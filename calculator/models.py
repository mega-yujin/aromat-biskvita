from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Component(models.Model):
    class Meta:
        verbose_name_plural = 'Компоненты'

    name = models.CharField(max_length=255, verbose_name='Название')
    units = models.CharField(max_length=50, verbose_name='Единица измрения')

    def __str__(self):  # строковое представление объекта модели
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
    diameter = models.IntegerField(null=True, blank=True, verbose_name='Диаметр')
    length = models.IntegerField(null=True, blank=True, verbose_name='Длина')
    width = models.IntegerField(null=True, blank=True, verbose_name='Ширина')
    components = models.ManyToManyField(Component, through='Ingredients', through_fields=('recipe', 'component'),
                                        verbose_name='Ингредиенты')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # return "/recipe/%s/" % self.pk
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

    def name(self):  # функциональное поле "name"
        return self.recipe.name + "(%s)" % self.component.name


class RecipeStatistic(models.Model):
    class Meta:
        verbose_name_plural = 'Статистика просмотров'
        # unique_together = (('recipe', 'user'),)

    recipe = models.OneToOneField(Recipe, on_delete=models.CASCADE)
    # user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    # date = models.DateTimeField(verbose_name='Дата просмотра', default=timezone.now)
    views = models.IntegerField(verbose_name='Просмотры', default=0)

    def __str__(self):
        return self.recipe.name


# class Favorites(models.Model):
#     class Meta:
#         verbose_name_plural = 'Избранные рецепты'
#
#     user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
#     recipe = models.ForeignKey(Recipe, verbose_name='Рецепт', on_delete=models.CASCADE)