
from django.urls import path
from .views import (
    CategoryListView, 
    SoftwareListView, 
    SoftwareDetailView, 
)

app_name = "software"

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),

    path('list/', SoftwareListView.as_view(), name='software-list'),

    path('detail/<slug:slug>/', SoftwareDetailView.as_view(), name='software-detail'),

]