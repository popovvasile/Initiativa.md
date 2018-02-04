# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include
 
from . import views


urlpatterns = patterns('',
	url(r'^$', views.news, name='news'),
    url(r'^(?P<pk>\d+)/$', views.NewsDetailView.as_view(), name='news_detail'),

    

)