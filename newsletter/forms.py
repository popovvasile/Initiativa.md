# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm

from newsletter.models import Petition


class CreatePetitionForm(forms.ModelForm):
    class Meta:
        model = Petition
        exclude = ('allow_comments', 'height_field', 'width_field', 'required_votes','posted','pub_date','data_limita','yes_votes','no_votes')

class ContactForm(forms.Form):
	full_name = forms.CharField(required=True, label = "Numele și prenumele")
	email = forms.EmailField()
	message = forms.CharField(widget=forms.Textarea, label = "Mesajul")


class PetitionForm(forms.Form):
    name = forms.CharField(label="Numele")
    surname = forms.CharField(label="Prenumele")


    petition_level = forms.ChoiceField(
            choices=(
            (0, "Național"),
            (1, "Regional/Municipal"),
            (2, 'Local'),), 
            label="Nivelul petiției", 
            required=True) 
    
    petition_topic = forms.ChoiceField(
            choices=(
            (0,"Transport/Roads"),
            (1,"Infrastructure"),
            (2,"Safety"),
            (3,"Consumers & Service"),
            (4,"Regional/Municipality"),
            (5,"Population & Migration"),
            (6,"Justice"),
            (7,"Economics"),
            (8,"Education & Science"),
            (9,"Governmental administration"),
            (10,"Governmental support"),
            (11,"Business"),
            (12,"Ecology"),
            (13,"Governmental support"),
            (14,"Health"),), 
            label="Subiectul", 
            required=True) 


    


    region = forms.ChoiceField(
            choices=(
            (0,"Municipiul Chişinău"),
            (1,"Municipiul Bălţi"),
            (2,"Municipiul Comrat"),
            (3,"Municipiul Tiraspol"),
            (4,"Municipiul Tighina (Bender)"),
            (5,"Anenii Noi"),
            (6,"Basarabeasca"),
            (7,"Briceni"),
            (8,"Cahul"),
            (9,"Călăraşi"),
            (10,"Cantemir"),
            (11,"Căuşeni"),
            (12,"Cimişlia"),
            (13,"Donduşeni"),
            (14,"Drochia"),
            (15,"Dubasari"),
            (16,"Edineţ"),
            (17,"Făleşti"),
            (18,"Floreşti"),
            (19,"Glodeni"),
            (20,"Hînceşti"),
            (21,"Ialoveni"),
            (22,"Leova"),
            (23,"Nisporeni"),
            (24,"Ocniţa"),
            (25,"Orhei"),
            (26,"Rezina"),
            (27,"Rîşcani"),
            (28,"Sîngerei"),
            (29,"Şoldăneşti"),
            (30,"Soroca"),
            (31,"Ştefan Vodă"),
            (32,"Străşeni"),
            (33,"Taraclia"),
            (34,"Teleneşti"),
            (35,"Ungheni"),), 
            label="Raion/Municipiu", 
            required=True) 
            


    petition = forms.CharField(widget=forms.Textarea, label="Problema", 
            required=True)
    impact = forms.CharField(widget=forms.Textarea, label="Impactul", 
            required=True)
    solution = forms.CharField(widget=forms.Textarea, label="Soluția", 
            required=True)











