# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include

from . import views


urlpatterns = patterns('',
	url(r'^$', views.petitions, name='petitions'),

    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='petition_results'),
    url(r'^thanks/$', views.petitionthanks, name='petition-thanks'),
    url(r'^(?P<petition_id>\d+)/yesvote/$', views.petition_yes_vote, name='petition_yes_vote'),
    url(r'^(?P<petition_id>\d+)/novote/$', views.petition_no_vote, name='petition_no_vote'),

)
