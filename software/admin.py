from django.contrib import admin
from .models import *

from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Tag, Software, Feature, SoftwareRelease, FilePart

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'icon_preview')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)

    # نمایش تصویر آیکون در لیست
    def icon_preview(self, obj):
        if obj.icon:
            return format_html('<img src="{}" style="width: 30px; height: 30px;" />', obj.icon.url)
        return "-"
    icon_preview.short_description = "آیکون"

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)

class FeatureInline(admin.TabularInline):
    model = Feature
    extra = 1

@admin.register(Software)
class SoftwareAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'developer', 'download_count', 'cover_preview', 'created_at')
    list_filter = ('category', 'developer', 'tags')
    search_fields = ('title', 'short_description', 'description')
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ['category', 'tags']
    readonly_fields = ('download_count',)
    inlines = [FeatureInline]
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'slug', 'cover_image', 'short_description', 'category', 'developer', 'tags')
        }),
        ('محتوا و آموزش', {
            'fields': ('description', 'installation_guide')
        }),
        ('آمار', {
            'fields': ('download_count',)
        }),
    )

    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" style="width: 50px; height: 30px; border-radius: 4px;" />', obj.cover_image.url)
        return "-"
    cover_preview.short_description = "کاور"

class FilePartInline(admin.TabularInline):
    model = FilePart
    extra = 1
    fields = ('part_number', 'file_size', 'download_link', 'download_count')
    readonly_fields = ('download_count',)

@admin.register(SoftwareRelease)
class SoftwareReleaseAdmin(admin.ModelAdmin):
    list_display = ('software', 'version', 'platform', 'part_count', 'is_active')
    list_filter = ('platform', 'is_active', 'software__category')
    search_fields = ('software__title', 'version')
    list_editable = ('is_active',)
    autocomplete_fields = ['software']
    
    inlines = [FilePartInline]

    def part_count(self, obj):
        return obj.parts.count()
    part_count.short_description = "تعداد پارت"


@admin.register(FilePart)
class FilePartAdmin(admin.ModelAdmin):
    list_display = ('release', 'part_number', 'file_size', 'download_count')
    search_fields = ('release__software__title',)
    list_filter = ('release__platform',)