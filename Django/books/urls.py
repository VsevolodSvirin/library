from django.conf.urls import url

from Django.books import views

urlpatterns = [
    url(r'^$', views.books_add, name='books_add'),
]
