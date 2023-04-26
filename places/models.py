from django.db import models
from tinymce.models import HTMLField


class Place(models.Model):
    title = models.CharField('Название места', max_length=200)
    description_short = models.TextField('Краткое описание', blank=True)
    description_long = HTMLField('Полное описание', blank=True)
    latitude = models.FloatField('Широта')
    longitude = models.FloatField('Долгота')

    def __str__(self):
        return self.title


class Image(models.Model):
    image = models.ImageField('Изображение')
    place = models.ForeignKey(Place,
                              on_delete=models.CASCADE,
                              null=True,
                              blank=True,
                              verbose_name='Название места',
                              related_name='images')
    position = models.IntegerField('Позиция', db_index=True)

    def __str__(self):
        return f'{self.position} {self.place}'

    class Meta:
        ordering = ('position',)