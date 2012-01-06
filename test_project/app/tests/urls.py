from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import direct_to_template


urlpatterns = patterns('',
                       url(r'^test-compress-templatetags/$',
                           direct_to_template,
                           {'template': 'test.html'},
                           name='test-compress-templatetags'),
                       )
