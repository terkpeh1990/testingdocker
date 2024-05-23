from django import forms
from .models import *
from django.forms.widgets import NumberInput


class PurchaseRquisitionForm(forms.ModelForm):
       
    quantity = forms.IntegerField(label=False)
    unit_price=forms.FloatField(label=False) 
    class Meta:
        model = PurchaseRequisition
        fields = ('purchase_requisition_date','quantity','unit_price')


class DecisionRquisitionForm(forms.ModelForm):
       
    reason = forms.CharField(
    widget=forms.Textarea(attrs={'maxlength': 1200}),
        label=False,required=True)
    class Meta:
        model = PurchaseRequisition_Suppliers
        fields = ('reason',)

class QoutationForm(forms.ModelForm):
    amount=forms.FloatField(label=False) 
    class Meta:
        model = PurchaseRequisition_Suppliers
        fields = ('amount',)