from django.contrib import admin
from django.utils.html import format_html
from mptt.admin import DraggableMPTTAdmin


from . import models


@admin.register(models.PostFilesModel)
class PostFilesAdmin(admin.ModelAdmin):
    """ Регистрация модели Файлов к постам в админке """
    list_display = ('title', 'code', 'download_count',)
    search_fields = ('title',)
    exclude = ('download_count',)
    readonly_fields = ('code',)


@admin.register(models.CategoryModel)
class CategoryAdmin(DraggableMPTTAdmin):
    """ Регистрация модели Категории в админке """
    list_display = ('tree_actions', 'indented_title', 'parent',)
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)


@admin.register(models.PostModel)
class PostAdmin(admin.ModelAdmin):
    """ Регистрация модели Постов в админке """
    list_display = ('title', 'image_preview', 'author', 'category', 'publish', 'created',
                    'updated', 'views', 'status',)
    list_filter = ('status', 'publish', 'author',)
    search_fields = ('title', 'body',)
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish'
    ordering = ('status', '-publish',)
    exclude = ("author", 'views',)

    def save_model(self, request, obj, form, change):
        """
        Переопределение метода save().
        При сохранении объекта, подставляет текущего пользователя в поле author
        """
        obj.author = request.user
        obj.save()
        super().save_model(request, obj, form, change)

    def image_preview(self, obj):
        """ Метод, добавляющий превью изображения к посту на странице в админке """
        if obj.image:
            return format_html(f'<img src="{obj.image.url}" width="100"/>')
        else:
            return '(No image found)'

    image_preview.short_description = 'Превью'


@admin.register(models.SocialLinksModel)
class SocialLinksAdmin(admin.ModelAdmin):
    """ Регистрация модели Ссылок в админке """
    list_display = ('title', 'image_preview', 'link')

    def image_preview(self, obj):
        """ Метод, добавляющий превью изображения к ссылке на странице в админке """
        if obj.image:
            return format_html(f'<img src="{obj.image.url}" width="64"/>')
        else:
            return '(No image found)'

    image_preview.short_description = 'Логотип'
