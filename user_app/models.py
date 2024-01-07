from datetime import datetime
from urllib import request

from PIL import Image
from django.contrib.auth.models import User
from django.db import models


class ProfileModel(models.Model):
    class Genders(models.TextChoices):
        UNDEFINED = 'U', 'не выбран'
        MALE = 'M', 'мужской'
        FEMALE = 'F', 'женский'

    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='profile',
                                verbose_name='Пользователь')
    gender = models.CharField(max_length=1,
                              choices=Genders.choices,
                              default=Genders.UNDEFINED,
                              verbose_name='Пол')
    dob = models.DateField(blank=True,
                           null=True,
                           verbose_name='Дата рождения')
    site_link = models.URLField(max_length=200,
                                blank=True,
                                null=True,
                                verbose_name='Ссылка на сайт')
    telegram_link = models.URLField(max_length=200,
                                    blank=True,
                                    null=True,
                                    verbose_name='Ссылка на Telegram',
                                    unique=True)
    user_avatar = models.ImageField(upload_to='user/avatars/',
                                    blank=True,
                                    null=True,
                                    verbose_name='Аватар пользователя')

    show_email = models.BooleanField(default=False,
                                     verbose_name='Отображать Email?')
    show_telegram = models.BooleanField(default=False,
                                        verbose_name='Отображать Telegram?')
    show_last_name = models.BooleanField(default=False,
                                         verbose_name='Отображать фамилию?')

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def save(self, *args, **kwargs):
        if not self.user_avatar:
            image_url = f'https://robohash.org/{self.user.username}'
            response = request.urlopen(image_url)
            self.user_avatar.save(f'{self.user.username}.png', response, save=False)
        super().save(*args, **kwargs)

        img = Image.open(self.user_avatar.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.user_avatar.path)

    def get_on_site(self):
        delta = datetime.now() - self.user.date_joined.replace(tzinfo=None)
        years = delta.days // 365
        months = (delta.days % 365) // 30
        days = (delta.days % 365) % 30
        if delta.days == 0:
            return 'меньше суток'
        else:
            on_site_string = ""
            if years > 0:
                on_site_string += f"{years} лет, "
            if months > 0:
                on_site_string += f"{months} месяца, "
            if days > 0:
                on_site_string += f"{days} дней"

            return on_site_string

    def get_telegram_username(self):
        return self.telegram_link.split('/')[-1]

    def get_age(self):
        if self.dob:
            today = datetime.today()
            age = today.year - self.dob.year

            if today.month < self.dob.month:
                age -= 1
            elif today.month == self.dob.month and today.day < self.dob.day:
                age -= 1

            return age

    def __str__(self):
        return self.user.username
