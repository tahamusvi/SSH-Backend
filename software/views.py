from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q, F

from .models import Category, Software, FilePart
from .serializers import (
    CategorySerializer, 
    SoftwareListSerializer, 
    SoftwareDetailSerializer
)

class CategoryListView(APIView):
    """
    Returns a list of all available categories.
    """
    permission_classes = [] 

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SoftwareListView(APIView):
    """
    Returns a paginated list of software with search and filtering capabilities.
    Query Parameters:
    - category: Filter by category slug (e.g., ?category=development)
    - search: Search in title, description, or tags (e.g., ?search=python)
    - page: Page number for pagination
    """
    permission_classes = []

    def get(self, request):
        queryset = Software.objects.all().order_by('-created_at')

        # 1. Filtering by Category
        category_slug = request.query_params.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        # 2. Searching
        search_query = request.query_params.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(short_description__icontains=search_query) |
                Q(tags__title__icontains=search_query)
            ).distinct()

        # 3. Pagination
        paginator = PageNumberPagination()
        paginator.page_size = 12 
        
        result_page = paginator.paginate_queryset(queryset, request)
        if result_page is not None:
            serializer = SoftwareListSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)

        # Fallback if pagination is not applicable
        serializer = SoftwareListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SoftwareDetailView(APIView):
    """
    Returns full details of a specific software identified by its slug.
    """
    permission_classes = []

    def get(self, request, slug):
        software = get_object_or_404(Software, slug=slug)
        serializer = SoftwareDetailSerializer(software)
        return Response(serializer.data, status=status.HTTP_200_OK)

