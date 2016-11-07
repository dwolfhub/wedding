from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'rsvp', views.rsvp, name="rsvp"),
]