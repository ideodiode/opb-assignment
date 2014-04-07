from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'guardresults.views.home_page', name='home_page'),
    url(r'^search/', 'guardresults.views.search', name='search'),
    url(r'^related_search/', 'guardresults.views.related_search', name='related_search'),
)
