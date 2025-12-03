from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug', 'icon']

class SoftwareListSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField() 
    
    latest_version = serializers.SerializerMethodField()
    
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Software
        fields = [
            'id', 'title', 'slug', 'cover_image', 
            'short_description', 'category', 
            'download_count', 'latest_version', 'rating'
        ]

    def get_latest_version(self, obj):
        last_release = obj.releases.filter(is_active=True).last()
        return last_release.version if last_release else "N/A"

    def get_rating(self, obj):
        return 4.8


class FilePartSerializer(serializers.ModelSerializer):
    download_url = serializers.SerializerMethodField()

    class Meta:
        model = FilePart
        fields = ['part_number', 'file_size', 'download_url']

    def get_download_url(self, obj):
        from django.urls import reverse
        # mock
        return "reverse('software-download', args=[obj.id])"

class SoftwareReleaseSerializer(serializers.ModelSerializer):
    parts = FilePartSerializer(many=True, read_only=True)

    class Meta:
        model = SoftwareRelease
        fields = ['id', 'version', 'platform', 'specific_install_guide', 'parts']

class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ['text']

class SoftwareDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    tags = serializers.StringRelatedField(many=True)
    features = FeatureSerializer(many=True, read_only=True)
    releases = SoftwareReleaseSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Software
        fields = [
            'id', 'title', 'slug', 'cover_image', 
            'description',
            'installation_guide',
            'developer',
            'category', 
            'download_count',
            'rating',
            'tags',
            'features',
            'releases',
            'updated_at'
        ]

    def get_rating(self, obj):
        return 4.9