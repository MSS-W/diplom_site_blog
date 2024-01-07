from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from taggit.models import Tag

from . import models


class PostSitemap(Sitemap):
    """ Класс карты сайта для постов """
    def items(self):
        """ Метод, возвращающий список объектов для карты сайта """
        return models.PostModel.post_manager.get_queryset()

    def lastmod(self, obj):
        """ Метод, возвращающий дату последней модификации объекта """
        return obj.updated

    def priority(self, obj):
        """ Метод, возвращающий приоритет объекта """
        return 0.8

    def changefreq(self, obj):
        """ Метод, возвращающий показатель частоты обновления объекта """
        return "weekly"

    def location(self, obj):
        """ Метод, возвращающий прямую ссылку на страницу объекта """
        return reverse('blog:post_page', args=[obj.category.slug, obj.slug])


class CategorySitemap(Sitemap):
    """ Класс карты сайта для Категорий """
    def items(self):
        """ Метод, возвращающий список объектов для карты сайта """
        return models.CategoryModel.objects.all()

    def priority(self, obj):
        """ Метод, возвращающий приоритет объекта """
        return 0.7

    def changefreq(self, obj):
        """ Метод, возвращающий показатель частоты обновления объекта """
        return "daily"

    def location(self, obj):
        """ Метод, возвращающий прямую ссылку на страницу объекта """
        return reverse('blog:category_page', args=[obj.slug])


class TagSitemap(Sitemap):
    """ Класс карты сайта для тегов """
    def items(self):
        """ Метод, возвращающий список объектов для карты сайта """
        return Tag.objects.all()

    def priority(self, obj):
        """ Метод, возвращающий приоритет объекта """
        return 0.5

    def location(self, obj):
        """ Метод, возвращающий прямую ссылку на страницу объекта """
        return reverse('blog:tag_page', args=[obj.slug])