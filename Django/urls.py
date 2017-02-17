from django.conf.urls import include, url

from Django.books import urls as book_urls

urlpatterns = [
    url(r'^books/', include(book_urls), name='books'),
]
