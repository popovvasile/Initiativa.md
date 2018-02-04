# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from django.template import RequestContext
from urllib import quote_plus #python 2
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.views import generic
from signals import petition_saved
from .forms import ContactForm, CreatePetitionForm
from django.contrib.auth.decorators import login_required

from .models import  *
# Create your views here.



def home(request):

	context = {


		'petition' : Petition.objects.all()[:5],

		'law' : Law.objects.all()[:5],


		'news' : News.objects.all()[:2],
		# 'news2' : News.objects.all()[3:6],
		# 'news3' : News.objects.all()[4:6],


	}

	return render(request, "index.html", context)

def laws(request):

    context = {


        'law' : Law.objects.all()[:3],
        'law_hidden' : Law.objects.all()[3:6],



    }

    return render(request, "laws.html", context)

def petitions(request):

    context = {


        'petition' : Petition.objects.all()[:3],
        'petition_hidden' : Petition.objects.all()[3:6],



    }

    return render(request, "petitions.html", context)
def news(request):

    context = {


        'news' : News.objects.all()[:2],
        'news2' : News.objects.all()[2:4],
        'news3' : News.objects.all()[4:6],
        'news4' : News.objects.all()[6:8],

    }

    return render(request, "news_list.html", context)



def contact(request):
    title = 'Contactează-ne'
    title_align_center = True
    form_contact = ContactForm(request.GET or None)
    message='Mulţumim pentru feedback! Vă vom raspunde cât mai curând. '
    context = {

        "form": form_contact,
        "title": title,
        "title_align_center": title_align_center,

    }


    if request.method =="GET" and form_contact.is_valid():
        # for key, value in form.cleaned_data.iteritems():
        #   print key, value
        #   #print form.cleaned_data.get(key)
        email = form_contact.cleaned_data.get("email")
        form_message = form_contact.cleaned_data.get("message")
        form_full_name = form_contact.cleaned_data.get("full_name")
        # print email, message, full_name
        subject = 'Site contact form'

        form_email = "popovvasile@gmail.com"


        from_email = settings.EMAIL_HOST_USER
        to_email = [from_email]
        
        contact_message = "%s: %s via %s"%( 
                form_full_name, 
                form_message, 
                email,)

        send_mail(subject, 
                contact_message, 
                from_email, 
                to_email, 
                html_message=contact_message,
                fail_silently=True)


        form_contact = ContactForm()
        context = {

        "form": form_contact,
        "title": title,
        "title_align_center": title_align_center,
        "message":message,
        }



    return render(request, "contact.html", context)





class About(generic.TemplateView):
    template_name = 'about.html'
















#petitions







class NewsDetailView(generic.DetailView):
    model = News
    template_name = 'news_detail.html'

    def get_queryset(self):
        """
        Excludes any petitions that aren't published yet.
        """
        return News.objects.filter(pub_date__lte=timezone.now())



class DetailView(generic.DetailView):
    model = Petition
    template_name = 'detail.html'

    
    def get_queryset(self):
        """
        Excludes any petitions that aren't published yet.
        """

        return Petition.objects.filter(pub_date__lte=timezone.now())


    # def get_context_data(self, **kwargs):
    #     context = super(DetailView, self).get_context_data(**kwargs)
    #     context.update({'next': reverse('comments-xtd-sent')})
    #     return context



class ResultsView(generic.DetailView):
    model = Petition
    template_name = 'results.html'




def petition_yes_vote(request, petition_id):
    p = get_object_or_404(Petition, pk=petition_id)
    if PetitionVoter.objects.filter(petition_id=petition_id, user_id=request.user.id).exists():

        return render(request, 'detail.html', {
            'petition': p,
            'error_message': "Scuze, dar deja aţi votat"
        })

    else:
        p.yes_votes += 1
        p.save()
        PetitionVoter.objects.create(petition_id=petition_id, user_id=request.user.id)

        return HttpResponseRedirect(reverse('petitions:petition_results', args=(p.id,)))


def petition_no_vote(request, petition_id):
    p = get_object_or_404(Petition, pk=petition_id)
    if PetitionVoter.objects.filter(petition_id=petition_id, user_id=request.user.id).exists():

        return render(request, 'detail.html', {
            'petition': p,
            'error_message': "Scuze, dar deja aţi votat"
        })

    else:
        p.yes_votes += 1
        p.save()
        PetitionVoter.objects.create(petition_id=petition_id, user_id=request.user.id)

        return HttpResponseRedirect(reverse('petitions:petition_results', args=(p.id,)))






class LawDetailView(generic.DetailView):
    model = Law
    template_name = 'law_detail.html'

    def get_queryset(self):
        """
        Excludes any petitions that aren't published yet.
        """
        return Law.objects.filter(pub_date__lte=timezone.now())


class LawResultsView(generic.DetailView):
    model = Law
    template_name = 'law_results.html'






def law_yes_vote(request, law_id):
    p = get_object_or_404(Law, pk=law_id)
    if Voter.objects.filter(law_id=law_id, user_id=request.user.id).exists():

        return render(request, 'law_detail.html', {
            'law': p,
            'error_message': "Scuze, dar deja aţi votat"
        })

    else:
        p.yes_votes += 1
        p.save()
        Voter.objects.create(law_id=law_id, user_id=request.user.id)

        return HttpResponseRedirect(reverse('laws:law_results', args=(p.id,)))



def law_no_vote(request, law_id):
    p = get_object_or_404(Law, pk=law_id)

    if Voter.objects.filter(law_id=law_id, user_id=request.user.id).exists():

        return render(request, 'law_detail.html', {
        'law': p,
        'error_message': "Scuze, dar deja aţi votat"
        })

    else:
        p.no_votes += 1
        p.save()
        Voter.objects.create(law_id=law_id, user_id=request.user.id)
        return HttpResponseRedirect(reverse('laws:law_results', args=(p.id,)))




# def add_comment_to_petition(request, pk):
#     post = get_object_or_404(Petition, pk=pk)
#     if request.method == "POST":
#         form = PetitionCommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.post = post
#             comment.save()
#             return render(request, 'thanks_for_comment.html')
#     else:
#         form = PetitionCommentForm()
#     return render(request, 'add_comment_to_petition.html', {'form': form})


# def add_comment_to_law(request, pk):
#     post = get_object_or_404(Law, pk=pk)
#     if request.method == "POST":
#         form = LawCommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.post = post
#             comment.save()
#             return render(request, 'thanks_for_comment.html')
#     else:
#         form = LawCommentForm()
#     return render(request, 'add_comment_to_law.html', {'form': form})












# def add_petition(request):
# 	title = 'Add Petition'
# 	title_align_center = True
# 	thanks = "Mulțumim pentru petiție!"
# 	gresit = "Completați toată informația."
# 	form_petition = PetitionForm(request.POST or None)
# 	if request.method =="POST" and form_petition.is_valid():
		 
# 		name = form_petition.cleaned_data.get("name")
# 		surname = form_petition.cleaned_data.get("surname")
# 		petition_level = form_petition.cleaned_data.get("petition_level")
# 		petition_topic = form_petition.cleaned_data.get("petition_topic")
# 		region = form_petition.cleaned_data.get("region")
# 		petition = form_petition.cleaned_data.get("petition")
# 		impact = form_petition.cleaned_data.get("impact")
# 		solution = form_petition.cleaned_data.get("solution")
# 		# print email, message, full_name
# 		subject = 'Site petition form'
# 		from_email = settings.EMAIL_HOST_USER
# 		to_email = [from_email]
		


# 		form_email = "popovvasile@gmail.com"
  
# 		some_html_message = "<div>%s,</div><div>%s,</div><div>%s,</div></td><div>%s,</div><div>%s,</div><h1>Petition</h1><div>%s,</div><h1>Impact</h1><div>%s,</div><h1>Solution</h1><div>%s,</div>"%( 
# 				name,
# 				surname,
# 				petition_level,
# 				petition_topic,
# 				region,
# 				petition,
# 				impact,
# 				solution,)

# 		send_mail(subject, 
# 				some_html_message, 
# 				from_email, 
# 				to_email, 
# 				html_message = some_html_message,
# 				fail_silently =True)
# 		form_petition = PetitionForm()





# 	context = {
# 		"form_petition": form_petition,
# 		"thanks":gresit,
        
# 		"title": title,
# 		"title_align_center": title_align_center,
		 



# 	}
# 	if request.method =="POST":
# 		context = {
# 		"form_petition": form_petition,
# 		"thanks":thanks,
        
# 		"title": title,
# 		"title_align_center": title_align_center,
# 		}
		 


# 	return render(request, "add-petition.html", context )








def create_new_petition(request, form_class = CreatePetitionForm,
            template_name = 'petitions/new_petition.html'):
    """
    This view will allow users to create a new petition.
    A User needs to be logged in to create a new petition.
    
    request -- the Request object
    form_class -- The Form Class to use for creating a new Petition
    template_name -- A custom template to use to display the petition creation form
    """
    if request.POST:
        petition_form = form_class(request.POST)
        if petition_form.is_valid():
            petition = petition_form.save(commit = False)
            petition.creator = request.user
            petition.save()

            petition_saved.send(sender = Petition, petition_form = petition_form, petition = petition)

            return HttpResponseRedirect(reverse('petitions:petition-thanks'))
    else:
        petition_form = form_class()
    return render_to_response("add-petition.html", {'petition_form' : petition_form},context_instance=RequestContext(request))


class PetitionThanksView(generic.DetailView):

    template_name = 'thanks_petition.html'




def petitionthanks(request):

    context = {}

    return render(request, 'thanks_petition.html', context)






from django.shortcuts import render_to_response
from django.template import RequestContext


def handler404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response



def csrf_failure(request, reason=""):
    
    return render_to_response("registration/registration_complete.html")

