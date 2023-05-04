import logging

import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

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


def get_or_create_place(place_description):
    defaults = {
        'description_short': place_description.get('description_short', ''),
        'description_long': place_description.get('description_long', ''),
    }
    place, created = Place.objects.get_or_create(title=place_description['title'],
                                                 latitude=place_description['coordinates']['lat'],
                                                 longitude=place_description['coordinates']['lng'],
                                                 defaults=defaults)
    logging.warning(f'New place "{place_description["title"]}" has been created')
    return place, created


class Command(BaseCommand):
    help = 'Автозагрузчик данных из *.json файла | *.json file data autoloader'

    def add_arguments(self, parser):
        parser.add_argument('url', metavar='B', type=str, help='*.json url')
        parser.add_argument('--skip_img', action='store_true', help='skips image upload')

    def handle(self, *args, **options):
        url = options['url']
        response = requests.get(url)
        response.raise_for_status()

        logging.warning(f'Response code: {response.status_code}')

        place_description = response.json()
        place, created = get_or_create_place(place_description)
        if options['skip_img']:
            logging.warning('Pictures uploading has been skipped...')
            return
        if created:
            upload_images(place_description['imgs'], place)
