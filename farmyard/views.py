from django.views.generic import DetailView, ListView

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from notes.forms import BriefNoteForm

from farmyard.models import Animal, Breed,  Milking


class BreedDetailView(DetailView):
    model = Breed

    def get_queryset(self, *args, **kwargs):
        return Breed.objects.filter(genus__slug=self.kwargs['genus_slug'])


class MilkingListView(ListView):
    model = Animal

    def get_queryset(self, *args, **kwargs):
        try:
            #animal = Animal.objects.get(self.kwargs.get('slug', None))
            qs = Milking.objects.filter(
                animal__primary_breed__genus__slug=self.kwargs['genus_slug'],
                animal__primary_breed__slug=self.kwargs['breed_slug'],
                animal__slug=self.kwargs['slug'])
        except:
            try:
                qs = Milking.objects.filter(
                    animal__primary_breed__genus__slug=self.kwargs['genus_slug'],
                    animal__primary_breed__slug=self.kwargs['breed_slug'],
                    animal__uuid__contains=self.kwargs['slug'])
            except:
                qs = None
        return qs


class AnimalDetailView(DetailView):
    model = Animal

    def get_queryset(self, *args, **kwargs):
        return Animal.objects.filter(
            primary_breed__genus__slug=self.kwargs['genus_slug'],
            primary_breed__slug=self.kwargs['breed_slug'])

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        pk = self.kwargs.get('pk', None)
        slug_or_uuid = self.kwargs.get('slug', None)
        if pk is not None:
            queryset = queryset.filter(pk=pk)

        # Next, try looking up by slug.
        elif slug_or_uuid is not None:
            try:
                obj = queryset.filter(uuid__contains=slug_or_uuid)[0]
            except:
                try:
                    obj = queryset.get(slug=slug_or_uuid)
                except ObjectDoesNotExist:
                    raise Http404(
                        (u"No %(verbose_name)s found matching the query") %
                        {'verbose_name': queryset.model._meta.verbose_name})

        # If none of those are defined, it's an error.
        else:
            raise AttributeError(u"Generic detail view %s must be called with "
                                 u"either an object pk or a slug."
                                 % self.__class__.__name__)

        return obj

    def get_context_data(self, **kwargs):
        context = super(AnimalDetailView, self).get_context_data(**kwargs)
        context['note_form'] = BriefNoteForm()
        return context
