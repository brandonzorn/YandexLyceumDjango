__all__ = []
from django.contrib import admin

import catalog.models


class ItemInline(admin.TabularInline):
    model = catalog.models.Item


@admin.register(catalog.models.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = [
        catalog.models.Item.name.field.name,
        catalog.models.Item.is_published.field.name,
        'image_tmb_display',
    ]
    list_editable = [catalog.models.Item.is_published.field.name]
    list_display_links = [catalog.models.Item.name.field.name]
    filter_horizontal = [
        catalog.models.Item.tags.field.name,
        catalog.models.Item.images.field.name,
    ]

    @admin.display(description='превью')
    def image_tmb_display(self, obj):
        if obj.main_image:
            return obj.main_image.image_tmb()
        return 'Нет изображения'


@admin.register(catalog.models.Tag)
class TagAdmin(admin.ModelAdmin):
    readonly_fields = [catalog.models.Tag.normalized_name.field.name]


@admin.register(catalog.models.Category)
class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = [catalog.models.Category.normalized_name.field.name]


@admin.register(catalog.models.MainImage)
class MainImageAdmin(admin.ModelAdmin):
    inlines = [
        ItemInline,
    ]
