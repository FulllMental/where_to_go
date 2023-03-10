import http

from django.shortcuts import render, get_object_or_404
from places.models import Place, Image
from django.http import HttpResponse, JsonResponse


def show_index(request):
    all_places = Place.objects.all()
    place_position = []
    for place in all_places:
        place_position.append(
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [place.latitude, place.longitude]
                },
                "properties": {
                    "title": place.title,
                    "placeId": place.pk,
                    "detailsUrl": "static/places/moscow_legends.json"
                }
            }
        )

    context = {
        'places_geojson': {
            "type": "FeatureCollection",
            "features": place_position
        }
    }

    return render(request, 'index.html', context)


def show_json(request, place_id):
    place = get_object_or_404(Place, pk=place_id)
    place_images = Image.objects.filter(place_title=place)
    images_urls = [image.image.url for image in place_images]
    response = JsonResponse(
        {
            "title": place.title,
            "imgs": images_urls,
            "description_short": place.description_short,
            "description_long": place.description_long,
            "coordinates": {
                "lat": place.latitude,
                "lon": place.longitude
            }
        },
        json_dumps_params={
            'ensure_ascii': False,
            'indent': 2
        }
    )
    return response
