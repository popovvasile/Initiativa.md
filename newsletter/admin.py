# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.

from dynamic_scraper.models import *
from .models import *

from django import forms
from forms import *
from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site


# from django.utils.translation import ugettext_lazy as _

# from django_comments_xtd.admin import XtdCommentsAdmin

class NewsAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': ['title', 'content', 'image'],
        }),

        ('Date information', {
            'fields': ['pub_date'],

        }),

    ]

    list_display = ('title', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['title']
    date_hierarchy = 'pub_date'


class PetitionAdmin(admin.ModelAdmin):
    list_display = ('question', 'pub_date', 'was_published_recently', 'posted')
    list_filter = ['pub_date']
    search_fields = ['question']
    date_hierarchy = 'pub_date'
    list_editable = ['posted']


class LawAdmin(admin.ModelAdmin):
    list_display = ('question', 'pub_date', 'data_limita', 'was_published_recently', 'posted')
    list_filter = ['pub_date', 'data_limita']
    search_fields = ['question']
    date_hierarchy = 'pub_date'
    list_editable = ['posted']


admin.site.register(Petition, PetitionAdmin)

admin.site.register(News, NewsAdmin)

admin.site.register(Law, LawAdmin)

# admin.site.register(ToScrapeWebsite)



admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.unregister(Site)

admin.site.unregister(ScrapedObjClass)
admin.site.unregister(Scraper)
admin.site.unregister(SchedulerRuntime)
admin.site.unregister(LogMarker)
admin.site.unregister(Log)
