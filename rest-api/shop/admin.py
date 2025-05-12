from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import Shop, Category, Product


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_user', 'get_title', 'get_description', 'image_preview', 'telegram_link')
    search_fields = ('user__telegram_id', 'user__id', 'user__username')
    readonly_fields = ('image_preview',)
    autocomplete_fields = ['user']

    def get_user(self, obj):
        return obj.user.username if obj.user else "-"
    get_user.short_description = 'User'
    
    def get_title(self, obj):
        return obj.get_title(language_code='uz')
    get_title.short_description = "Title (UZ)"
    
    def get_description(self, obj):
        return obj.get_description(language_code='uz')
    get_description.short_description = "Description (UZ)"
    
    def image_preview(self, obj):
        if obj.image and hasattr(obj.image, 'file'):
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.file.url)
        return "-"
    image_preview.short_description = "Image Preview"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop', 'get_title', 'get_description', 'image_preview')
    readonly_fields = ('image_preview',)

    def get_title(self, obj):
        return obj.get_title(language_code='uz')
    get_title.short_description = "Title (UZ)"
    
    def get_description(self, obj):
        return obj.get_description(language_code='uz')
    get_description.short_description = "Description (UZ)"
    
    def image_preview(self, obj):
        if obj.image and hasattr(obj.image, 'file'):
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.file.url)
        return "-"
    image_preview.short_description = "Image Preview"
    
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'get_title', 'get_description', 'image_preview', 'price')
    readonly_fields = ('image_preview',)

    def get_title(self, obj):
        return obj.get_title(language_code='uz')
    get_title.short_description = "Title (UZ)"
    
    def get_description(self, obj):
        return obj.get_description(language_code='uz')
    get_description.short_description = "Description (UZ)"
    
    def image_preview(self, obj):
        if obj.image and hasattr(obj.image, 'file'):
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.file.url)
        return "-"
    image_preview.short_description = "Image Preview"