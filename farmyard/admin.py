from django.forms import models
from django.contrib import admin
from django.contrib.contenttypes import generic

from notes.admin import NoteInline
from attributes.admin import clean_attribute_value

from farmyard.models import Farm, Genus, Breed, Animal, SecondaryBreed, \
    AnimalAttribute, AnimalAttributeOption, Milking


class AnimalAttributeInlineForm(models.ModelForm):

    def clean_value(self):
        return clean_attribute_value(self.cleaned_data,
                                     self.cleaned_data['animal'])


class AnimalAttributeInline(admin.TabularInline):
    model = AnimalAttribute
    #form = AnimalAttributeInlineForm


class SecondaryBreedInline(generic.GenericTabularInline):
    model = SecondaryBreed


class AnimalAdmin(admin.ModelAdmin):
    list_filter = ('owner_farm', 'breeder_farm', 'alt_owner', 'alt_breeder', )
    list_display = ('sex', 'name', 'dam', 'birthday', 'primary_breed',)
    inlines = [AnimalAttributeInline, SecondaryBreedInline, NoteInline, ]


class MilkingAdmin(admin.ModelAdmin):
    inlines = [NoteInline, ]

admin.site.register(Milking, MilkingAdmin)
admin.site.register(Animal, AnimalAdmin)
admin.site.register(Farm)
admin.site.register(Genus)
admin.site.register(Breed)
admin.site.register(AnimalAttribute)
admin.site.register(AnimalAttributeOption)
