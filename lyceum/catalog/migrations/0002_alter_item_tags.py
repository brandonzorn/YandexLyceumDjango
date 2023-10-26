# Generated by Django 4.2.6 on 2023-10-19 17:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="tags",
            field=models.ManyToManyField(
                help_text="Теги",
                related_name="items",
                to="catalog.tag",
                verbose_name="теги",
            ),
        ),
    ]