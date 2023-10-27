__all__ = []
from django.db import models


class AbstractModel(models.Model):
    is_published = models.BooleanField(
        'опубликовано',
        default=True,
        help_text='Опубликовано',
    )
    name = models.CharField(
        'название',
        max_length=150,
        unique=True,
        help_text='Название',
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class AbstractAttributeModel(AbstractModel):
    normalized_name = models.CharField(
        max_length=200,
        unique=True,
        help_text='Уникальное имя',
    )

    class Meta:
        abstract = True
