from django.contrib import admin
from django.utils.html import format_html
from .models import *
from .forms import *


class VendorAdmin(admin.ModelAdmin):
    list_display = ('shop_name', 'name', 'email_id', 'shop_address', 'package', 'payment_status')
    search_fields = ('shop_name', 'name', 'email_id')

    def save_model(self, request, obj, form, change):
        # Optionally, handle vendor-specific logic
        super().save_model(request, obj, form, change)


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'description', 'qr_code']

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

class AddressAdmin(admin.ModelAdmin):
    # Define which fields to display in the list view
    list_display = ('vendor', 'shop_number', 'street', 'area', 'city', 'state', 'pincode', 'is_default', 'full_address')
    list_filter = ('is_default',)
    search_fields = ('vendor__shop_name', 'shop_number', 'street', 'area', 'city', 'state', 'pincode')

    # Adding full_address method to display the complete address in the list view
    def full_address(self, obj):
        return obj.full_address()
    full_address.short_description = 'Full Address'  # Title for the full address column

    # Allow editing of the full address fields directly in the admin form
    fieldsets = (
        (None, {
            'fields': ('vendor', 'shop_number', 'street', 'area', 'city', 'state', 'pincode', 'is_default')
        }),
    )

    # Make the address fields more user-friendly
    def save_model(self, request, obj, form, change):
        # You can add additional logic if needed before saving the address
        super().save_model(request, obj, form, change)

# Create a custom admin class for Order
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'design', 'vendor_name', 'vendor_shop_name', 'quantity', 'total_price', 'order_status', 'order_date')
    list_filter = ('order_status',)
    search_fields = ('design__title', 'vendor__name', 'vendor__shop_name')
    ordering = ('-order_date',)

    def vendor_name(self, obj):
        return obj.vendor.name if obj.vendor else 'N/A'
    vendor_name.admin_order_field = 'vendor__name'  # Allows sorting by vendor name
    vendor_name.short_description = 'Vendor Name'

    def vendor_shop_name(self, obj):
        return obj.vendor.shop_name if obj.vendor else 'N/A'
    vendor_shop_name.admin_order_field = 'vendor__shop_name'  # Allows sorting by shop name
    vendor_shop_name.short_description = 'Shop Name'


# Register the model and the custom admin class

# Registering models
admin.site.register(Design, DesignAdmin)
admin.site.register(SubCategory1)
admin.site.register(SubCategory2)
admin.site.register(SubCategory3)
admin.site.register(Category)
admin.site.register(Address, AddressAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(Order, OrderAdmin)
