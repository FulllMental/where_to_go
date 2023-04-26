from django.contrib import admin
from django.utils.html import format_html, mark_safe
from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminMixin, SortableAdminBase, SortableInlineAdminMixin

from .models import Place, Image


class ImageInline(SortableInlineAdminMixin, admin.StackedInline):
    extra = 1
    ordering = ['position']
    model = Image
    readonly_fields = ['place_image']
    fields = ['image', 'place_image']

    def place_image(self, Image):
        return format_html('<img src={} width={} height={}>',
                           mark_safe(Image.image.url),
                           Image.image.width // 3,
                           Image.image.height // 3)

    place_image.short_description = 'Превью'


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [ImageInline,]
    search_fields = ['title']