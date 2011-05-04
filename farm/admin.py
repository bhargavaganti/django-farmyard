import logging
from django.forms import models, ValidationError
from django.contrib import admin
from django.contrib.contenttypes import generic

from farm.models import Farm, Genus, Breed, Animal, Product, ProductType, Note, SecondaryBreed, AnimalAttribute, AnimalAttributeOption, ProductAttribute, ProductAttributeOption
from notes.admin import NoteInline
from attributes.admin import clean_attribute_value

class AnimalAttributeInlineForm(models.ModelForm):

    def clean_value(self):
        print 'Farm admin.py: cleaning values and have data: %s' % self.cleaned_data
        return clean_attribute_value(self.cleaned_data, self.cleaned_data['animal'])

class AnimalAttributeInline(admin.TabularInline):
    model = AnimalAttribute
    #form = AnimalAttributeInlineForm

class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute

class SecondaryBreedInline(generic.GenericTabularInline):
    model = SecondaryBreed

class AnimalAdmin(admin.ModelAdmin):
    inlines = [ AnimalAttributeInline, SecondaryBreedInline, NoteInline, ]

class ProductAdmin(admin.ModelAdmin):
    inlines = [ ProductAttributeInline, NoteInline, ]

admin.site.register(Animal, AnimalAdmin)
admin.site.register(Farm)
admin.site.register(Genus)
admin.site.register(Breed)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductType)
admin.site.register(AnimalAttributeOption)
admin.site.register(ProductAttributeOption)