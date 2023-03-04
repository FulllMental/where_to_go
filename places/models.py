from django.db import models


class Place(models.Model):
    title = models.CharField('Название места', max_length=200)
    description_short = models.TextField('Краткое описание')
    description_long = models.TextField('Полное описание')
    latitude = models.FloatField('Ширина')
    longitude = models.FloatField('Долгота')

    def __str__(self):
        return f'{self.title}'


class Image(models.Model):
    image = models.ImageField('Изображение', db_index=True)
    place_title = models.ForeignKey(Place,
                                    on_delete=models.CASCADE,
                                    null=True,
                                    blank=True,
                                    verbose_name='Название места',
                                    related_name='place_titles')

    def __str__(self):
        return f'{self.pk} {self.place_title}'
