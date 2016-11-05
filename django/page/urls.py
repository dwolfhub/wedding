from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'hotels.html', views.hotels, name="hotels"),
    url(r'venue.html', views.venue, name="venue"),
    url(r'wedding-day-info.html', views.wedding_day_info, name="wedding_day_info"),
    url(r'^$', views.save_the_date, name="save_the_date"),
]