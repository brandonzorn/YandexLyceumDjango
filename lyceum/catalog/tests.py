__all__ = []
from http import HTTPStatus

import django.core.exceptions
from django.test import Client, TestCase
from django.urls import reverse
from parameterized import parameterized

from catalog import models


class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category = models.Category.objects.create(
            name='Электроника',
            slug='elektronika',
        )
        cls.category.full_clean()
        cls.category.save()
        cls.item = models.Item(
            name='TestItem',
            category=cls.category,
            text='Text превосходно',
        )
        cls.item.full_clean()
        cls.item.save()

    def test_catalog_endpoint(self):
        response = Client().get('/catalog/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_catalog_index_endpoint(self):
        response = Client().get('/catalog/1/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    @parameterized.expand(
        [
            ('123', HTTPStatus.OK),
            ('-123', HTTPStatus.NOT_FOUND),
            ('fff', HTTPStatus.NOT_FOUND),
            ('0', HTTPStatus.NOT_FOUND),
            ('0123', HTTPStatus.NOT_FOUND),
            ('!123', HTTPStatus.NOT_FOUND),
        ],
    )
    def test_catalog_re_num_endpoint(self, value, expected_code):
        response = Client().get(f'/catalog/re/{value}/')
        self.assertEqual(response.status_code, expected_code, msg=value)

    @parameterized.expand(
        [
            ('123', HTTPStatus.OK),
            ('-123', HTTPStatus.NOT_FOUND),
            ('fff', HTTPStatus.NOT_FOUND),
            ('0', HTTPStatus.NOT_FOUND),
            ('0123', HTTPStatus.NOT_FOUND),
            ('!123', HTTPStatus.NOT_FOUND),
        ],
    )
    def test_catalog_converter_endpoint(self, value, expected_code):
        response = Client().get(f'/catalog/converter/{value}/')
        self.assertEqual(response.status_code, expected_code)


class ReverseURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category = models.Category.objects.create(
            name='Электроника',
            slug='elektronika',
        )
        cls.category.full_clean()
        cls.category.save()
        cls.item = models.Item(
            name='TestItem',
            category=cls.category,
            text='Text превосходно',
        )
        cls.item.full_clean()
        cls.item.save()

    def test_item_detail_reverse_url(self):
        url = reverse('catalog:item_detail', args=[1])
        response = Client().get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)


class ModelTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.category = models.Category.objects.create(
            name='Электроника',
            slug='elektronika',
        )
        cls.category.full_clean()
        cls.category.save()
        cls.tag = models.Tag.objects.create(
            name='Безрамочный',
            slug='bezramochnyy',
        )
        cls.tag.full_clean()
        cls.tag.save()
        cls.tag1 = models.Tag.objects.create(
            name='Высокое качество изображения',
            slug='vysokoe_kachestvo_izobrazheniya',
        )
        cls.tag1.full_clean()
        cls.tag1.save()

    def test_one_item(self):
        item_count = models.Item.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.item = models.Item(
                name='Смартфон Apple iPhone 12 Pro',
                category=self.category,
                text='Смартфон Apple iPhone 12 Pro: '
                'превосходный смартфон с передовыми функциями.',
            )
            self.item.full_clean()
            self.item.save()
            self.item.tags.add(ModelTests.tag, ModelTests.tag1)
            self.item.save()
        self.assertEqual(models.Item.objects.count(), item_count)

    def test_create(self):
        item_count = models.Item.objects.count()
        self.item = models.Item(
            name='Смартфон Apple iPhone 12 Pro',
            category=self.category,
            text='Смартфон Apple iPhone 12 Pro: '
            'превосходно смартфон с передовыми функциями.',
        )
        self.item.full_clean()
        self.item.save()
        self.item.tags.add(ModelTests.tag, ModelTests.tag1)
        self.item.save()
        self.assertEqual(models.Item.objects.count(), item_count + 1)

    @parameterized.expand(
        [
            ('Test tag1', 'test/slug'),
            ('Test_tag2', '/!'),
            ('Test-tag3', 'slug+test'),
            ('Test_123_tag', '/slug'),
        ],
    )
    def test_error_tag(self, name, slug):
        tag_count = models.Tag.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.tag = models.Tag(name=name, slug=slug)
            self.tag.full_clean()
            self.tag.save()
        self.assertEqual(models.Tag.objects.count(), tag_count)

    @parameterized.expand(
        [
            ('Test tag1', 'test_slug'),
            ('Test_tag2', 'testslug'),
            ('Test-tag3', 'test-_slug_te123_-st333'),
            ('Test_123_tag', '1234567890'),
        ],
    )
    def test_valid_tag(self, name, slug):
        tag_count = models.Tag.objects.count()
        self.tag = models.Tag(name=name, slug=slug)
        self.tag.full_clean()
        self.tag.save()
        self.assertEqual(models.Tag.objects.count(), tag_count + 1)

    @parameterized.expand(
        [
            ('Test category1', 'test/slug'),
            ('Test_category2', '/---!'),
            ('Test-category3', 'slug+test'),
            ('Test_123_category4', '/slug'),
        ],
    )
    def test_error_category(self, name, slug):
        category_count = models.Category.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.category = models.Category(name=name, slug=slug)
            self.category.full_clean()
            self.category.save()
        self.assertEqual(models.Category.objects.count(), category_count)

    @parameterized.expand(
        [
            ('Test category1', 'test_slug'),
            ('Test_category2', 'testslug'),
            ('Test-category3', 'test_slug_te123_st333'),
            ('Test_123_category4', '1234567890'),
        ],
    )
    def test_valid_category(self, name, slug):
        category_count = models.Category.objects.count()
        self.category = models.Category(name=name, slug=slug)
        self.category.full_clean()
        self.category.save()
        self.assertEqual(models.Category.objects.count(), category_count + 1)

    @parameterized.expand(
        [
            ('Category1', 'slug', 'category1', 'slug1'),
            ('Category2', 'slug', 'сategory2', 'slug1'),
        ],
    )
    def test_normalized_name_category_error(self, name, slug, name1, slug1):
        with self.assertRaises(django.core.exceptions.ValidationError):
            # ca кириллицей
            self.category = models.Category(name=name, slug=slug)
            self.category.full_clean()
            self.category.save()
            # ca латиницей
            self.category1 = models.Category(name=name1, slug=slug1)
            self.category1.full_clean()
            self.category1.save()
