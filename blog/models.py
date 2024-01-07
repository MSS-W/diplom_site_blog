import random

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field
from mptt.managers import TreeManager
from mptt.models import MPTTModel, TreeForeignKey
from taggit.managers import TaggableManager


class PostManager(models.Manager):
    """ Менеджер постов """

    def get_queryset(self):
        """ Переопределённый метод менеджера, возвращающий только опубликованные посты """
        return super().get_queryset().filter(status=PostModel.Status.PUBLISHED)

    def latest_posts(self):
        """ Метод, возвращающий пять последних опубликованных постов """
        return super().get_queryset().filter(status=PostModel.Status.PUBLISHED)[:5]

    def popular_posts(self):
        """ Метод, возвращающий пять самых просматриваемых постов """
        return super().get_queryset().filter(status=PostModel.Status.PUBLISHED).order_by('-views')[:5]


class PostFilesModel(models.Model):
    """Модель файлов для поста"""
    title = models.CharField(max_length=200,
                             verbose_name='Имя файла')
    file = models.FileField(upload_to='post_files/')
    code = models.IntegerField(default=0,
                               verbose_name='Код файла',
                               unique=True)
    download_count = models.IntegerField(default=0,
                                         verbose_name='Скачиваний')

    objects = models.Manager()

    class Meta:
        verbose_name = 'Файл поста'
        verbose_name_plural = 'Файлы постов'

    def save(self, *args, **kwargs):
        """
        Переопределённый метод save().
        При сохранении объекта записывает в поле code сгенерированный код.
        """
        if not self.code:
            self.code = self.generate_unique_code()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_unique_code():
        """ Статический метод для генерации случайного уникального кода """
        code = random.randint(100000, 999999)
        while PostFilesModel.objects.filter(code=code).exists():
            code = random.randint(100000, 999999)
        return code

    def increment_download_count(self):
        """Метод увеличения счётчика загрузок"""
        self.download_count += 1
        self.save()

    def __str__(self):
        return self.title


class CategoryModel(MPTTModel):
    """Модель категории"""
    title = models.CharField(max_length=100,
                             verbose_name="Заголовок")
    slug = models.SlugField(verbose_name="Альт. заголовок")
    parent = TreeForeignKey('self',
                            on_delete=models.CASCADE,
                            null=True,
                            blank=True,
                            related_name='children',
                            db_index=True,
                            verbose_name='Родительская категория')
    description = CKEditor5Field(max_length=350,
                                 verbose_name="Описание",
                                 blank=True)

    objects = TreeManager()

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        unique_together = [['parent', 'slug']]
        verbose_name = 'Категория поста'
        verbose_name_plural = 'Категории постов'

    def get_absolute_url(self):
        """Метод получения URL-адреса объекта"""
        return reverse('blog:category_page', args=[self.slug])

    def __str__(self):
        return self.title


class PostModel(models.Model):
    """Модель поста"""

    class Status(models.TextChoices):
        """Класс выбора статуса поста"""
        DRAFT = 'ЧЕ', 'Черновик'
        PUBLISHED = 'ОП', 'Опубликовано'

    title = models.CharField(max_length=200,
                             verbose_name="Заголовок")
    slug = models.SlugField(verbose_name="Альт. заголовок")
    image = models.ImageField(upload_to='post/%Y/%m/%d',
                              default='default/not_found.png',
                              verbose_name='Изображение поста')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='post',
                               verbose_name="Автор")
    category = TreeForeignKey('CategoryModel',
                              on_delete=models.PROTECT,
                              related_name='post',
                              verbose_name='Категория')
    short_body = CKEditor5Field(max_length=350,
                                verbose_name="Краткое описание",
                                blank=True)
    full_body = CKEditor5Field(verbose_name='Содержимое поста')
    publish = models.DateTimeField(default=timezone.now,
                                   verbose_name="Опубликовано")
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name="Создано")
    updated = models.DateTimeField(auto_now=True,
                                   verbose_name="Обновлено")
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT,
                              verbose_name="Статус")
    views = models.IntegerField(default=0,
                                verbose_name="Количество просмотров")
    telegram_link = models.CharField(max_length=300,
                                     verbose_name="Ссылка на Telegram",
                                     blank=True,
                                     null=True)
    file = models.OneToOneField("PostFilesModel",
                                on_delete=models.SET_NULL,
                                null=True,
                                blank=True,
                                verbose_name="Файл",
                                related_name="post")
    tags = TaggableManager(blank=True)

    objects = models.Manager()
    post_manager = PostManager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def get_absolute_url(self):
        """Метод получения URL-адреса объекта"""
        return reverse('blog:post_page', args=[self.category.slug, self.slug])

    def get_next_post(self):
        """Метод получения следующего поста"""
        try:
            return self.get_next_by_publish(category=self.category)
        except PostModel.DoesNotExist:
            return None

    def get_previous_post(self):
        """Метод получения предыдущего поста"""
        try:
            return self.get_previous_by_publish(category=self.category)
        except PostModel.DoesNotExist:
            return None

    def __str__(self):
        return self.title


class SocialLinksModel(models.Model):
    """ Модель для ссылок """
    title = models.CharField(max_length=50,
                             verbose_name="Название")
    image = models.ImageField(upload_to='social-links/',
                              default='default/not_found.png',
                              verbose_name='Изображение ссылки')
    link = models.CharField(max_length=300,
                            verbose_name="Ссылка")

    objects = models.Manager()

    class Meta:
        verbose_name = 'Ссылка'
        verbose_name_plural = 'Ссылки'

    def __str__(self):
        return self.title
