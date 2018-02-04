# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include

from . import views


urlpatterns = patterns('',
	url(r'^$', views.laws, name='laws'),

    url(r'^(?P<pk>\d+)/$', views.LawDetailView.as_view(), name='law_detail'),
    url(r'^(?P<pk>\d+)/results/$', views.LawResultsView.as_view(), name='law_results'),
    url(r'^(?P<law_id>\d+)/yesvote/$', views.law_yes_vote, name='law_yes_vote'),
    url(r'^(?P<law_id>\d+)/novote/$', views.law_no_vote, name='law_no_vote'),

)
