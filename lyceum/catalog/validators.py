__all__ = []
import re

import django.core.exceptions
from django.utils.deconstruct import deconstructible


@deconstructible
class MustContainValidator:
    def __init__(self, *args):
        self.must_contain = args

    def __eq__(self, other):
        return self.must_contain == other.must_contain and isinstance(
            other,
            MustContainValidator,
        )

    def __call__(self, value):
        must_contain_str = '|'.join(self.must_contain)
        pattern = fr'\b({must_contain_str})\b'
        if not re.search(pattern, value.lower()):
            raise django.core.exceptions.ValidationError(
                f'В тексте {value} должно быть {must_contain_str}',
            )


@deconstructible
class RangeValidator:
    val_range = None

    def __init__(self, min_value: int, max_value: int):
        if min_value is not None and max_value is not None:
            self.val_range = range(min_value, max_value)

    def __eq__(self, other):
        return self.val_range == other.val_range and isinstance(
            other,
            RangeValidator,
        )

    def __call__(self, value):
        if value not in self.val_range:
            raise django.core.exceptions.ValidationError(
                f'Число {value} не в диапазоне от 0 до 32767',
            )


def chars_validator(value):
    if not re.fullmatch(r'^[A-Za-z0-9_-]+$', value):
        raise django.core.exceptions.ValidationError(
            f'Текст {value} не соответствует паттерну',
        )
