# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils import timezone

from django.utils.text import slugify

from dynamic_scraper.models import Scraper, SchedulerRuntime
from scrapy_djangoitem import DjangoItem

import datetime
from django.utils import timezone
# # Create your models here.

from django.contrib.auth.models import User


class ToScrapeWebsite(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()
    scraper = models.ForeignKey(Scraper, blank=True, null=True, on_delete=models.SET_NULL)
    scraper_runtime = models.ForeignKey(SchedulerRuntime, blank=True, null=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return self.name

def upload_location(instance, filename):
    #filebase, extension = filename.split(".")
    #return "%s/%s.%s" %(instance.id, instance.id, extension)
    NewsModel = instance.__class__
    try:
        new_id = NewsModel.objects.order_by("id").last().id + 1
    except:
        new_id =  1
    """
    instance.__class__ gets the model News. We must use this method because the model is defined below.
    Then create a queryset ordered by the "id"s of each object, 
    Then we get the last object in the queryset with `.last()`
    Which will give us the most recently created Model instance
    We add 1 to it, so we get what should be the same id as the the news we are creating.
    """
    return "%s/%s" %(new_id, filename)

def one_day_hence():
    return timezone.now() + timezone.timedelta(days=30)

class News(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    content = models.TextField()
    image = models.ImageField(upload_to=upload_location, 
        null=True, 
        blank=True, 
        default="Proiectul_Hotararii_de_Guvern.jpg")


    def __unicode__(self):  # Python 3: def __str__(self):
        return self.title

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date < now
    class Meta:
        verbose_name = 'New'

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def get_absolute_url(self):
        return "/news/%i/" % self.id


    
# class NewsComment(models.Model):
#     post = models.ForeignKey(News, related_name='ncomments')
#     author = models.CharField(max_length=200)
#     text = models.TextField()
#     created_date = models.DateTimeField(default=timezone.now)
#     approved_comment = models.BooleanField(default=False)

#     def approve(self):
#         self.approved_comment = True
#         self.save()

#     def __str__(self):
#         return self.text



class Petition(models.Model):

    PETITION_LEVEL_CHOICES=(
            ('0', "Național"),
            ('1', "Regional/Municipal"),
            ('2', 'Local'),)

    PETITION_TOPIC_CHOICES=(
            ('0',"Transport/Roads"),
            ('1',"Infrastructure"),
            ('2',"Safety"),
            ('3',"Consumers & Service"),
            ('4',"Regional/Municipality"),
            ('5',"Population & Migration"),
            ('6',"Justice"),
            ('7',"Economics"),
            ('8',"Education & Science"),
            ('9',"Governmental administration"),
            ('10',"Governmental support"),
            ('11',"Business"),
            ('12',"Ecology"),
            ('13',"Governmental support"),
            ('14',"Health"),)
    PETITION_REGION_CHOICES=(
            ('0',"Municipiul Chişinău"),
            ('1',"Municipiul Bălţi"),
            ('2',"Municipiul Comrat"),
            ('3',"Municipiul Tiraspol"),
            ('4',"Municipiul Tighina (Bender)"),
            ('5',"Anenii Noi"),
            ('6',"Basarabeasca"),
            ('7',"Briceni"),
            ('8',"Cahul"),
            ('9',"Călăraşi"),
            ('10',"Cantemir"),
            ('11',"Căuşeni"),
            ('12',"Cimişlia"),
            ('13',"Donduşeni"),
            ('14',"Drochia"),
            ('15',"Dubasari"),
            ('16',"Edineţ"),
            ('17',"Făleşti"),
            ('18',"Floreşti"),
            ('19',"Glodeni"),
            ('20',"Hînceşti"),
            ('21',"Ialoveni"),
            ('22',"Leova"),
            ('23',"Nisporeni"),
            ('24',"Ocniţa"),
            ('25',"Orhei"),
            ('26',"Rezina"),
            ('27',"Rîşcani"),
            ('28',"Sîngerei"),
            ('29',"Şoldăneşti"),
            ('30',"Soroca"),
            ('31',"Ştefan Vodă"),
            ('32',"Străşeni"),
            ('33',"Taraclia"),
            ('34',"Teleneşti"),
            ('35',"Ungheni"),)

    posted = models.BooleanField(verbose_name='Posteaza', default=False)
    question = models.CharField(max_length=200,verbose_name="Titlul petiţiei")
    pub_date = models.DateTimeField('date published',default=timezone.now)
    data_limita = models.DateTimeField('data limita a votului',default=one_day_hence)


    name = models.CharField(max_length=100,verbose_name="Numele")
    surname = models.CharField(max_length=100,verbose_name="Prenumele")
    user_email = models.CharField(max_length=100,verbose_name="Email")
    petition_level = models.CharField(max_length=100, verbose_name="Alege nivelul petiției", choices=PETITION_LEVEL_CHOICES,default="Naţional")
    petition_topic = models.CharField(max_length=100, verbose_name="Alege domeniul petiției",choices=PETITION_TOPIC_CHOICES)
    petition_region = models.CharField(max_length=100, verbose_name="Daca petiţia e de nivel regional sau local, alege raionul/municipiul ",null=True, blank=True,choices=PETITION_REGION_CHOICES)
    petition_local = models.CharField(max_length=100, verbose_name="Daca petiţia e de nivel local, scrie denumirea exactă a localităţii ",null=True, blank=True)

    content = models.TextField(verbose_name="Descrierea problemei")
    impact = models.TextField(verbose_name="Impactul")
    solution = models.TextField(verbose_name="Soluţia")
    required_votes = models.IntegerField(default=100)

    


    allow_comments = models.BooleanField('allow comments', default=True)


    image = models.ImageField(upload_to=upload_location, 
        null=True, 
        blank=True, 
        width_field="width_field", 
        height_field="height_field",
        default="Proiectul_Hotararii_de_Guvern.jpg")

    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.question

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date < now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def voting_ends(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.data_limita < now

    voting_ends.admin_order_field = 'data_limita'
    yes_votes = models.IntegerField(default=0)
    no_votes = models.IntegerField(default=0)
    def get_absolute_url(self):
        return "/petitions/%i/" % self.id

def petition_post_save_callback(sender, **kwargs):
    """
    This listener exists so that we can create a slug for every new petition.
    We check if a slug exists for the given petition. If it doesn't, we 
    use django.template.defaultfilters.slugify to create a slug from the title.
    If the generated slug exists in the DB, then we join in the petition's id 
    into the slug and save the petition, else we just use the slug create from
    the title as the object's slug_name
    """
    petition = kwargs.pop('instance')
    created = kwargs.pop('created')

    if created:
        
            

            petition.save()
    
models.signals.post_save.connect(petition_post_save_callback, sender = Petition)


class Law(models.Model):

    LAW_LEVEL_CHOICES=(
            ('0', "Național"),
            ('1', "Regional/Municipal"),
            ('2', 'Local'),)
    question = models.CharField(max_length=400,default="")
    pub_date = models.DateTimeField('date published',default=timezone.now)
    data_limita = models.DateTimeField('data limita a votului',default=one_day_hence)
    content = models.TextField(default="", blank=True)
    impact = models.TextField(default="", blank=True)
    solution = models.TextField(default="", blank=True)
    required_votes = models.IntegerField(default=100)
    image = models.ImageField(upload_to=upload_location, 
        null=True, 
        blank=True, 
        width_field="width_field", 
        height_field="height_field",
        default="Proiectul_Hotararii_de_Guvern.jpg")
    posted = models.BooleanField(verbose_name='Posteaza', default=False)
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.question

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date < now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def voting_ends(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.data_limita < now

    voting_ends.admin_order_field = 'data_limita'



    law_level = models.CharField(max_length=100,blank=True,verbose_name="Alege nivelul legii",default="Naţional",choices=LAW_LEVEL_CHOICES)

    # news_website = models.ForeignKey(ToScrapeWebsite)
    url_proiect = models.URLField(default="http://particip.gov.md/")
    file_url_1= models.URLField(default="http://particip.gov.md/",blank=True)
    file_url_2= models.URLField(default="http://particip.gov.md/",blank=True)
    file_url_3= models.URLField(default="http://particip.gov.md/",blank=True)
    checker_runtime = models.ForeignKey(SchedulerRuntime, blank=True, null=True, on_delete=models.SET_NULL)


    yes_votes = models.IntegerField(default=0)
    no_votes = models.IntegerField(default=0)
    def get_absolute_url(self):
        return "/laws/%i/" % self.id






class PetitionVoter(models.Model):
    user = models.ForeignKey(User)
    petition = models.ForeignKey(Petition)



class Voter(models.Model):
    user = models.ForeignKey(User)
    law = models.ForeignKey(Law)

# class LawComment(models.Model):
#     law = models.ForeignKey(Law, related_name='law_comment')
#     author = models.CharField(max_length=200)
#     law_description = models.TextField()
#     law_impact = models.TextField()
#     law_problems = models.TextField()
#     created_date = models.DateTimeField(default=timezone.now)
#     approved_comment = models.BooleanField(default=False)
#     expert_comment = models.BooleanField(default=False)

#     def approve(self):
#         self.approved_comment = True
#         self.save()

#     def expert(self):
#         self.approved_comment = True
#         self.save()
#     def __str__(self):
#         return self.law_description








class ArticleItem(DjangoItem):
    django_model = Law






