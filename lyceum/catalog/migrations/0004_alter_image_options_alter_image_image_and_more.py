# Generated by Django 4.2.6 on 2023-10-25 04:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0003_image_item_images_item_main_image"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="image",
            options={
                "verbose_name": "изображение",
                "verbose_name_plural": "изображения",
            },
        ),
        migrations.AlterField(
            model_name="image",
            name="image",
            field=models.ImageField(
                upload_to="%Y%m%d/", verbose_name="изображение"
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="images",
            field=models.ManyToManyField(
                blank=True,
                help_text="Неограниченное количество изображений",
                related_name="items",
                to="catalog.image",
                verbose_name="фотогалерея",
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="main_image",
            field=models.OneToOneField(
                blank=True,
                help_text="Крупная картинка товара",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="catalog.image",
                verbose_name="главное изображение",
            ),
        ),
    ]
