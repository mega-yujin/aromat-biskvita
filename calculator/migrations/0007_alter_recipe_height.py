# Generated by Django 3.2.6 on 2021-12-10 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0006_auto_20211210_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='height',
            field=models.FloatField(blank=True, null=True, verbose_name='Высота'),
        ),
    ]