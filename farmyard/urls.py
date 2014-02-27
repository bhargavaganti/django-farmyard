from django.conf import settings
from django.conf.urls import *
from django.views.generic import DetailView, ListView
from farmyard.views import BreedDetailView, AnimalDetailView, MilkingListView
from farmyard.models import Animal, Genus, Breed, RegistrationBody, AnimalRegistration


# custom views vendors
urlpatterns = patterns('',
    url(r'^animals/$', view=ListView.as_view(model=Genus), name="fm-genus-list"),
	url(r'^animals/(?P<slug>[-\w]+)/$', view=DetailView.as_view(model=Genus), name="fm-genus-detail"),
	url(r'^animals/(?P<slug>[-\w]+)/$', view=DetailView.as_view(model=Genus), name="fm-genus-detail"),
	url(r'^animals/(?P<genus_slug>[-\w]+)/(?P<slug>[-\w]+)/$', view=BreedDetailView.as_view(), name="fm-breed-detail"),
	url(r'^animals/(?P<genus_slug>[-\w]+)/(?P<breed_slug>[-\w]+)/(?P<slug>[-\w]+)/$', view=AnimalDetailView.as_view(), name="fm-animal-detail"),
	url(r'^animals/(?P<genus_slug>[-\w]+)/(?P<breed_slug>[-\w]+)/(?P<slug>[-\w]+)/milkings/$', view=MilkingListView.as_view(), name="fm-milking-detail"),
)
