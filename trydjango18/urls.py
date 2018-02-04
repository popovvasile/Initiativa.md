# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.conf.urls import patterns
from newsletter import views
from django.conf.urls import handler404, handler500

handler404 = 'newsletter.views.handler404'
handler500 = 'newsletter.views.handler500'
urlpatterns = [
    # Examples:
	url(r'^$', 'newsletter.views.home', name='home'),
	url(r'^contact/$', 'newsletter.views.contact', name='contact'),
	url(r'^about/$', views.About.as_view(), name='about'),
	

	url(r'^noway/', include(admin.site.urls)),



	url(r'^petitions/', include('newsletter.petitions_urls', namespace="petitions")),
	url(r'^laws/', include('newsletter.laws_urls', namespace="laws")),
	url(r'^accounts/', include('registration.backends.default.urls')),

	url(r'^news/', include('newsletter.news_urls', namespace="news")),
	url(r'^petition-thanks/', views.PetitionThanksView.as_view(), name='thanks_petitions'),
	url(r'^addpetitions/', views.create_new_petition, name='add_petitions'),
	url(r'^comments/', include('fluent_comments.urls')),
	# url(r'^comments/posted/$', 'newsletter.views.comment_posted' )
	


]


if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if not settings.DEBUG:
	urlpatterns += patterns('',
	    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
	)
	urlpatterns += patterns('',
	    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
	)