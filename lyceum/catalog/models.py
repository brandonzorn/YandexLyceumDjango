__all__ = []
from ckeditor import fields
import django.core.exceptions
from django.db import models
from django.utils.safestring import mark_safe
from django_cleanup import cleanup
from sorl.thumbnail import get_thumbnail

from catalog import validators
from core import models as core_models
from core import utils as core_utils


class Tag(core_models.AbstractAttributeModel):
    slug = models.CharField(
        'слаг',
        max_length=200,
        unique=True,
        validators=[validators.chars_validator],
        help_text='Слаг',
    )

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def clean_fields(self, exclude=None):
        self.normalized_name = core_utils.normalize_text(self.name)
        if (
            Tag.objects.exclude(pk=self.pk)
            .filter(normalized_name=self.normalized_name)
            .exists()
        ):
            raise django.core.exceptions.ValidationError(
                'Значение уже существует.',
            )
        super().clean_fields(exclude)


class Category(core_models.AbstractAttributeModel):
    slug = models.CharField(
        'слаг',
        max_length=200,
        unique=True,
        validators=[validators.chars_validator],
        help_text='Слаг',
    )
    weight = models.IntegerField(
        'вес',
        default=100,
        validators=[validators.RangeValidator(1, 32767)],
        help_text='Вес',
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def clean_fields(self, exclude=None):
        self.normalized_name = core_utils.normalize_text(self.name)
        if (
            Category.objects.exclude(pk=self.pk)
            .filter(normalized_name=self.normalized_name)
            .exists()
        ):
            raise django.core.exceptions.ValidationError(
                'Значение уже существует.',
            )
        super().clean_fields(exclude)


@cleanup.select
class MainImage(models.Model):
    image = models.ImageField(verbose_name='изображение', upload_to='%Y%m%d/')

    def get_image_x300(self):
        return get_thumbnail(self.image, '300x300', crop='center')

    def image_tmb(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="50">')
        return 'Нет изображения'

    image_tmb.short_description = 'превью'
    image_tmb.allow_tags = True

    class Meta:
        verbose_name = 'изображение'
        verbose_name_plural = 'изображения'


class Item(core_models.AbstractModel):
    text = fields.RichTextField(
        'текст',
        validators=[
            validators.MustContainValidator('превосходно', 'роскошно'),
        ],
        help_text='Текст',
    )

    category = models.ForeignKey(
        Category,
        help_text='Категория',
        verbose_name='категория',
        on_delete=models.CASCADE,
    )
    tags = models.ManyToManyField(
        Tag,
        help_text='Теги',
        verbose_name='теги',
        related_name='items',
    )
    main_image = models.OneToOneField(
        MainImage,
        verbose_name='главное изображение',
        help_text='Крупная картинка товара',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    images = models.ManyToManyField(
        MainImage,
        verbose_name='фотогалерея',
        help_text='Неограниченное количество изображений',
        related_name='items',
        blank=True,
    )

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
