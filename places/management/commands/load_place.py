import logging
import os

import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from environs import Env

from places.models import Place, Image


def upload_images(img_urls, place):
    if not img_urls:
        logging.error('It seems, there is no images')
        return
    for index, img_url in enumerate(img_urls):
        image_name = img_url.split('/')[-1]
        response = requests.get(img_url)
        response.raise_for_status()
        image_content = ContentFile(response.content, name=image_name)
        Image.objects.create(image=image_content,
                             place=place,
                             position=index)
    logging.warning('All images has been uploaded')


def get_json(url):
    response = requests.get(url)
    response.raise_for_status()
    logging.warning(f'Response code: {response.status_code}')
    return response.json()


def create_place(response_json):
    defaults = {
        'description_short': response_json.get('description_short', 'Здесь должно было быть короткое описание'),
        'description_long': response_json.get('description_long', 'Здесь должно было быть длинное описание'),
    }
    place, _ = Place.objects.get_or_create(title=response_json['title'],
                                           latitude=response_json['coordinates']['lat'],
                                           longitude=response_json['coordinates']['lng'],
                                           defaults=defaults)
    logging.warning(f'New place "{response_json["title"]}" has been created')
    return place


class Command(BaseCommand):
    help = 'Автозагрузчик данных из *.json файла | *.json file data autoloader'

    def add_arguments(self, parser):
        parser.add_argument('url', metavar='B', type=str, help='*.json url')
        parser.add_argument('--skip_img', action='store_true', help='skips image upload')

    def handle(self, *args, **options):
        url = options['url']
        response_json = get_json(url)
        place = create_place(response_json)
        if options['skip_img']:
            logging.warning('Pictures uploading has been skipped...')
            return
        upload_images(response_json['imgs'], place)
