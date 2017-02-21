from django.conf.urls import include, url

from Django.books import urls as book_urls
from Django.readers import urls as reader_urls

urlpatterns = [
    url(r'^books', include(book_urls), name='books'),
    url(r'^readers', include(reader_urls), name='readers'),
]
