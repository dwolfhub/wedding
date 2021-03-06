from django.shortcuts import render

import logging


logger = logging.getLogger('django')


def __render_with_body_class(request, template):
    logger.info('%s page loaded' % request.resolver_match.url_name)
    return render(request, template, {
        'body_class': request.resolver_match.url_name
    })


def save_the_date(request):

    return __render_with_body_class(request, 'page/save-the-date.html')


def hotels(request):
    return __render_with_body_class(request, 'page/hotels.html')


def wedding_day_info(request):
    return __render_with_body_class(request, 'page/wedding-day-info.html')


def venue(request):
    return __render_with_body_class(request, 'page/venue.html')


def bridal_party(request):
    return __render_with_body_class(request, 'page/bridal-party.html')
