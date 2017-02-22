from django.conf.urls import url

from Django.books import views

urlpatterns = [
    url(r'^$', views.books_list, name='books_list'),
    # url(r"^/(?P<pk>[\d]+)/$", views.book_detail(), name="book_detail"),
]
