from django.db import models
from tinymce.models import HTMLField


class Place(models.Model):
    title = models.CharField('Название места', max_length=200)
    description_short = models.TextField('Краткое описание')
    description_long = HTMLField('Полное описание')
    latitude = models.FloatField('Широта')
    longitude = models.FloatField('Долгота')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        ordering = ('pk',)


class Image(models.Model):
    image = models.ImageField('Изображение', db_index=True)
    place_title = models.ForeignKey(Place,
                                    on_delete=models.CASCADE,
                                    null=True,
                                    blank=True,
                                    verbose_name='Название места',
                                    related_name='place_titles')
    position = models.IntegerField('Позиция', default=0)

    def __str__(self):
        return f'{self.position} {self.place_title}'

    class Meta:
        ordering = ('place_title',)
