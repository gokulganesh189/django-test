from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
import time
from django.db import connection, models
from django.utils.translation import gettext as _
from django.utils.translation import activate
import logging

logger = logging.getLogger(__name__)
# Create your views here.



def home(request):
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
    return HttpResponse("Check your logs!")

@api_view(['GET'])
def books_with_normal_filter(request):
    start_normal = time.time()
    books = Book.objects.all()
    print(connection.queries)  # Check executed queries
    data = []
    for book in books:
        # Each access to `publisher` or `authors` triggers a query
        publisher_name = book.publisher.name  # 1 query per book for publisher
        authors = [author.name for author in book.authors.all()]  # 1 query per book for authors
        print(connection.queries)  # Check executed queries
        data.append({
            "name": book.name,
            "publisher": publisher_name,
            "authors": authors
        })
    end_normal = time.time()
    print(end_normal-start_normal, "normal time")
    return Response(data)


@api_view(['GET'])
def books_with_prefetch_related(request):
    start_normal = time.time()
    books = Book.objects.select_related('publisher').prefetch_related('authors')
    # print(connection.queries)  # Check executed queries
    data = []
    for book in books:
        # No additional queries for accessing related data
        publisher_name = book.publisher.name
        authors = [author.name for author in book.authors.all()]
        # print(connection.queries)  # Check executed queries
        data.append({
            "name": book.name,
            "publisher": publisher_name,
            "authors": authors
        })
    end_normal = time.time()
    print(end_normal-start_normal, "prefetch time")
    return Response(data)

@api_view(['GET'])
def calculate_publishers(request):
    stores = Store.objects.prefetch_related('books').annotate(count=models.Sum('books__pages'))
    data = []
    for store in stores:
        store_name = store.name
        books = [book.name for book in store.books.all()]
        data.append({
            "store_name": store_name,
            "book_name": books,
            "page_count":store.count
        })
    return Response(data)

@api_view(['POST'])
def define_post(request):
    name = request.data['name']
    return Response({"name":name})

@api_view(['GET'])
def get_publisher(request):
    preferred_language = request.headers.get('Accept-Language', 'es')
    activate(preferred_language)
    books = Book.objects.all()
    message = _('all book names and publishers\' names')
    data = {
        "message": message,
        "books": [
            {
                "book_name": book.name,
                "publisher_name": book.publisher.name
            }
            for book in books
        ]
    }
    return Response(data)

# @api_view(['GET'])
# def get_publisher(request):
#     preferred_language = request.headers.get('Accept-Language', 'es')
#     activate(preferred_language)
#     books = Book.objects.select_related('publisher').filter(id=1).order_by('-id').first()
#     print(type(books), books)
#     message = _('all book names and publishers\' names')
#     data = {
#         "message": message,
#         "books": [
#             {
#                 "book_name": books.name,
#                 "publisher_name": books.publisher.name
#             }
#         ]
#     }
#     return Response(data)

# @api_view(['GET'])
# def get_publisher(request):
#     # Get preferred language from headers and activate it
#     preferred_language = request.headers.get('Accept-Language', 'es')
#     activate(preferred_language)
    
#     # Execute raw SQL query with LEFT JOIN
#     books = Book.objects.raw("""
#         SELECT user_book.id, user_book.name, user_publisher.name as publisher_name 
#         FROM user_book
#         LEFT JOIN user_publisher ON user_book.publisher_id = user_publisher.id
#     """)
    
#     # Process the results
#     book_data = [
#         {
#             "book_name": book.name,
#             "publisher_name": getattr(book, 'publisher_name', None)  # Use raw query alias
#         }
#         for book in books
#     ]
    
#     # Create the response message
#     message = _('All book names and publishers\' names')
#     data = {
#         "message": message,
#         "books": book_data
#     }
#     return Response(data)
