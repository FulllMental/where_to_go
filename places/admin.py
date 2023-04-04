from django.contrib import admin
from django.utils.html import format_html, mark_safe

from .models import Place, Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass


class ImageInline(admin.TabularInline):
    model = Image
    readonly_fields = ['place_image']
    fields = ['image', 'place_image', 'position']

    def place_image(self, Image):
        return format_html('<img src={} width={} height={}>',
                           mark_safe(Image.image.url),
                           Image.image.width // 3,
                           Image.image.height // 3)

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    inlines = [ImageInline]