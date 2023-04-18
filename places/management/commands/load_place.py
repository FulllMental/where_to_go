import logging

import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from environs import Env

from places.models import Place, Image


def upload_images(img_urls, new_place):
    if not img_urls:
        logging.error('It seems, there is no images')
        return
    for index, img_url in enumerate(img_urls):
        image_name = img_url.split('/')[-1]
        response = requests.get(img_url)
        response.raise_for_status()
        image_content = ContentFile(response.content, name=image_name)
        Image.objects.create(image=image_content,
                             place_title=new_place,
                             position=index)
    logging.warning('All images has been uploaded')


def get_json(url):
    response = requests.get(url)
    response.raise_for_status()
    logging.warning(f'Response code: {response.status_code}')
    response_json = response.json()
    new_place, _ = Place.objects.get_or_create(title=response_json['title'],
                                                description_short=response_json['description_short'],
                                                description_long=response_json['description_long'],
                                                latitude=response_json['coordinates']['lat'],
                                                longitude=response_json['coordinates']['lng'])
    logging.warning(f'New Place: {response_json["title"]} has been created')
    return new_place, response_json


class Command(BaseCommand):
    help = 'Автозагрузчик данных из *.json файла | *.json file data autoloader'

    def add_arguments(self, parser):
        parser.add_argument('url', metavar='B', type=str, help='*.json url')

    def handle(self, *args, **options):
        url = options['url']
        new_place, response_json = get_json(url)
        upload_images(response_json['imgs'], new_place)

