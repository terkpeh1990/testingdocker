import django_filters
from django import forms
from django_filters import DateFilter , CharFilter, NumberFilter,ModelChoiceFilter
from .models import *
from inventory.models import Categorys


class DateInput(forms.DateInput):
    input_type = 'date'

# def classification(request):
#     if request is None:
#         return Classification.objects.none()
#     else:
#         return Classification.objects.all()

# def category(request):
#     if request is None:
#         return Categorys.objects.none()
#     else:
#         return Categorys.objects.all()

class AssetsFilter(django_filters.FilterSet):
    classification = ModelChoiceFilter(field_name='classification', queryset=Classification.objects.all(),label='Select Classification')
    category = ModelChoiceFilter(field_name='product__category_id', queryset=Categorys.objects.all(),label='Select Category')
    sra = CharFilter(field_name='sra', lookup_expr='exact', label='SRA No.')
    
    # category = ModelChoiceFilter(field_name='product__category_id',queryset=classification)
  
    class Meta:
        model = FixedAsset
        fields = ['classification','category']
