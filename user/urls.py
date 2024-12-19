from .views import *
from django.urls import path


urlpatterns = [
    path('', home),
    path('books_with_normal_filter/', books_with_normal_filter),
    path('books_with_prefetch_related/', books_with_prefetch_related),
    path('calculate_publishers/', calculate_publishers),
    path('test_post/', define_post),
    path('publishers/', get_publisher),
]
