from django.shortcuts import render, get_object_or_404
from places.models import Place, Image
from django.http import JsonResponse
from django.urls import reverse


def show_index(request):
    all_places = Place.objects.all()
    place_positions = []
    for place in all_places:
        place_positions.append(
            {
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [place.longitude, place.latitude]
                },
                'properties': {
                    'title': place.title,
                    'placeId': place.id,
                    'detailsUrl': reverse('show_json', args=(place.pk,))
                }
            }
        )

    context = {
        'places_geojson': {
            'type': 'FeatureCollection',
            'features': place_positions
        }
    }

    return render(request, 'index.html', context)


def show_json(request, place_id):
    place = get_object_or_404(Place, pk=place_id)
    place_images = place.images.all()
    response = JsonResponse(
        {
            'title': place.title,
            'imgs': [image.image.url for image in place_images],
            'description_short': place.description_short,
            'description_long': place.description_long,
            'coordinates': {
                'lat': place.latitude,
                'lon': place.longitude
            }
        },
        json_dumps_params={
            'ensure_ascii': False,
            'indent': 2
        }
    )
    return response
