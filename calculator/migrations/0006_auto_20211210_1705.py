# Generated by Django 3.2.6 on 2021-12-10 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0005_auto_20211209_1909'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='height',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Высота'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='diameter',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Диаметр'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='length',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Длина'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='width',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Ширина'),
        ),
    ]
