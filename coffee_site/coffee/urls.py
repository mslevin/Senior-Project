from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^survey/$', views.survey, name='survey'),
        url(r'^submit/$', views.submit, name='submit'),
        url(r'^taste/$', views.taste, name='taste'),
        url(r'^recommend/$', views.recommend, name='recommend'),
    ]
