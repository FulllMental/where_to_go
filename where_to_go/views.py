from django.shortcuts import render
from places.models import Place


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
