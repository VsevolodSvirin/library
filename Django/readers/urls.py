from django.conf.urls import url

from Django.readers import views

urlpatterns = [
    url(r'^$', views.readers_list, name='readers_list'),
    url(r'^/(?P<pk>[\d]+)/$', views.reader_detail, name='reader_detail'),
]
