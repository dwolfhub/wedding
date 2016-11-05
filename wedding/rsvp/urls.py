from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'rsvp.html', views.rsvp, name="rsvp"),
]