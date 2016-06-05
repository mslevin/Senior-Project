from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^survey/$', views.survey, name='survey'),
        url(r'^submit/$', views.submit, name='submit'),
        url(r'^taste/$', views.TasteView.as_view(), name='taste'),
        url(r'^recommend/$', views.recommend, name='recommend'),
        url(r'^coffees/$', views.coffees, name='coffees'),
        url(r'^coffees/(?P<coffee_id>[0-9]+)/$', views.coffee_details, name="coffee_details"),
        url(r'^login/$', views.LoginView.as_view(), name='login'),
        url(r'^logout/$', views.logout_view, name='logout'),
        url(r'^profile/$', views.profile, name="profile")
    ]
