from django import forms
from .models import *
from authentication.models import User
from django.forms.widgets import NumberInput

class BudgetForm(forms.ModelForm):
    start = forms.DateField(widget=NumberInput(attrs={'type': 'date'}),label=False,required=True)
    end = forms.DateField(widget=NumberInput(attrs={'type': 'date'}),label=False,required=True)
    budget_amount = forms.FloatField(label=False) 
    
    class Meta:
        model = Annual_Budget
        fields = ('start','end','budget_amount')

    def clean(self, *args, **kwargs):
        budget_amount = self.cleaned_data['budget_amount']
        if budget_amount < 1:
            raise forms.ValidationError(
                    {'budget_amount': ["Amount Cannot be less than GHC 1.00 "]})
        return super(BudgetForm, self).clean(*args, **kwargs)


class Supply_Chain_RequisitionForm(forms.ModelForm):
    
    requisition_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}),label=False)
    class Meta:
        model = Supply_Chain_Requisition
        fields = ('requisition_date',)

class Supply_Chain_RequisitionDetailForm(forms.ModelForm):
    product = forms.CharField(label=False)
    unit_price = forms.FloatField(label=False) 
    quantity = models.IntegerField(default=1)
    class Meta:
        model = Supply_Chain_Requisition_Details
        fields = ('product','unit_price','quantity',)