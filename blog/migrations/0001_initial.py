# Generated by Django 4.2.2 on 2024-01-05 07:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_ckeditor_5.fields
import mptt.fields
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0005_auto_20220424_2025'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Заголовок')),
                ('slug', models.SlugField(verbose_name='Альт. заголовок')),
                ('description', django_ckeditor_5.fields.CKEditor5Field(blank=True, max_length=350, verbose_name='Описание')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='blog.categorymodel', verbose_name='Родительская категория')),
            ],
            options={
                'verbose_name': 'Категория поста',
                'verbose_name_plural': 'Категории постов',
                'unique_together': {('parent', 'slug')},
            },
        ),
        migrations.CreateModel(
            name='PostFilesModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Имя файла')),
                ('file', models.FileField(upload_to='post_files/')),
                ('code', models.IntegerField(default=0, unique=True, verbose_name='Код файла')),
                ('download_count', models.IntegerField(default=0, verbose_name='Скачиваний')),
            ],
            options={
                'verbose_name': 'Файл поста',
                'verbose_name_plural': 'Файлы постов',
            },
        ),
        migrations.CreateModel(
            name='SocialLinksModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Название')),
                ('image', models.ImageField(default='default/not_found.png', upload_to='social-links/', verbose_name='Изображение ссылки')),
                ('link', models.CharField(max_length=300, verbose_name='Ссылка')),
            ],
            options={
                'verbose_name': 'Ссылка',
                'verbose_name_plural': 'Ссылки',
            },
        ),
        migrations.CreateModel(
            name='PostModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Заголовок')),
                ('slug', models.SlugField(verbose_name='Альт. заголовок')),
                ('image', models.ImageField(default='default/not_found.png', upload_to='post/%Y/%m/%d', verbose_name='Изображение поста')),
                ('short_body', django_ckeditor_5.fields.CKEditor5Field(blank=True, max_length=350, verbose_name='Краткое описание')),
                ('full_body', django_ckeditor_5.fields.CKEditor5Field(verbose_name='Содержимое поста')),
                ('publish', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Опубликовано')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
                ('status', models.CharField(choices=[('ЧЕ', 'Черновик'), ('ОП', 'Опубликовано')], default='ЧЕ', max_length=2, verbose_name='Статус')),
                ('views', models.IntegerField(default=0, verbose_name='Количество просмотров')),
                ('telegram_link', models.CharField(blank=True, max_length=300, null=True, verbose_name='Ссылка на Telegram')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('category', mptt.fields.TreeForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='post', to='blog.categorymodel', verbose_name='Категория')),
                ('file', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='post', to='blog.postfilesmodel', verbose_name='Файл')),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'Пост',
                'verbose_name_plural': 'Посты',
                'ordering': ['-publish'],
                'indexes': [models.Index(fields=['-publish'], name='blog_postmo_publish_0e928c_idx')],
            },
        ),
    ]