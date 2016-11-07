from django.conf.urls import url
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy

from . import views

urlpatterns = [
    url(r'hotels$', views.hotels, name="hotels"),
    url(r'venue$', views.venue, name="venue"),
    url(r'wedding-day-info$', views.wedding_day_info, name="wedding_day_info"),
    url(r'^$', views.save_the_date, name="save_the_date"),
    url(r'hotels.html$', RedirectView.as_view(url='/hotels', permanent=True)),
    url(r'venue.html$', RedirectView.as_view(url='/venue', permanent=True)),
    url(r'wedding-day-info.html$',
        RedirectView.as_view(url=reverse_lazy('wedding_day_info'),
                             permanent=True)),
]