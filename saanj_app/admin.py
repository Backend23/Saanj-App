from django.contrib import admin
from django.utils.html import format_html
from .models import Design, Category, DesignImage, DesignVideo, SubCategory1, SubCategory2, SubCategory3
from .forms import DesignUploadForm

# Custom Filter for Price Range
class PriceRangeFilter(admin.SimpleListFilter):
    title = 'Price Range'
    parameter_name = 'price_range'

    def lookups(self, request, model_admin):
        return (
            ('10000-20000', '10,000 to 20,000'),
            ('21000-30000', '21,000 to 30,000'),
            ('31000-40000', '31,000 to 40,000'),
            ('41000-50000', '41,000 to 50,000'),
            ('51000-60000', '51,000 to 60,000'),
            ('61000-70000', '61,000 to 70,000'),
            # Add more ranges as needed
        )

    def queryset(self, request, queryset):
        if self.value() == '10000-20000':
            return queryset.filter(price__gte=10000, price__lte=20000)
        elif self.value() == '21000-30000':
            return queryset.filter(price__gte=21000, price__lte=30000)
        elif self.value() == '31000-40000':
            return queryset.filter(price__gte=31000, price__lte=40000)
        elif self.value() == '41000-50000':
            return queryset.filter(price__gte=41000, price__lte=50000)
        elif self.value() == '51000-60000':
            return queryset.filter(price__gte=51000, price__lte=60000)
        elif self.value() == '61000-70000':
            return queryset.filter(price__gte=61000, price__lte=70000)
        # Add more conditions for other ranges
        return queryset

# Inline for Images
class DesignImageInline(admin.TabularInline):
    model = DesignImage
    extra = 1
    readonly_fields = ['image_preview']
    fields = ('image', 'image_preview')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 100px; height: auto;" />', obj.image.url)
        return "No image"

    image_preview.short_description = 'Image Preview'

# Inline for Videos
class DesignVideoInline(admin.TabularInline):
    model = DesignVideo
    extra = 1
    readonly_fields = ['video_link']
    fields = ('video', 'video_link')

    def video_link(self, obj):
        if obj.video:
            return format_html('<a href="{}" target="_blank">View Video</a>', obj.video.url)
        return "No video"

    video_link.short_description = 'Video Link'

# Admin customization
class DesignAdmin(admin.ModelAdmin):
    form = DesignUploadForm
    inlines = [DesignImageInline, DesignVideoInline]
    list_display = ('title', 'category', 'description', 'price', 'subcategory1', 'subcategory2', 'subcategory3', 'display_images', 'display_videos')
    search_fields = ('title', 'category__name', 'subcategory1__name', 'subcategory2__name', 'subcategory3__name')
    list_filter = (PriceRangeFilter, 'category', 'subcategory1', 'subcategory2', 'subcategory3')
    ordering = ('-id',)

    # Method to display images in the list display
    def display_images(self, obj):
        images = obj.images.all()
        if images:
            return format_html(''.join([f'<img src="{img.image.url}" style="width: 50px; height: auto; margin-right: 5px;" />' for img in images]))
        return "No images"

    display_images.short_description = 'Images'

    # Method to display video links in the list display
    def display_videos(self, obj):
        videos = obj.videos.all()
        if videos:
            return format_html(''.join([f'<a href="{video.video.url}" target="_blank">Video {i+1}</a><br>' for i, video in enumerate(videos)]))
        return "No videos"

    display_videos.short_description = 'Videos'

# Registering models
admin.site.register(Design, DesignAdmin)
admin.site.register(SubCategory1)
admin.site.register(SubCategory2)
admin.site.register(SubCategory3)
admin.site.register(Category)
