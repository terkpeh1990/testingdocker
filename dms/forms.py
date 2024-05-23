from django import forms
from .models import *
from django.forms.widgets import NumberInput
from authentication.models import User
from .validators import validate_file_extension
from accounting.models import Currency
from inventory.models import Supplier

class FolderForm(forms.ModelForm):
    name = forms.CharField(label=False)

    class Meta:
        model = DocumentCategory
        fields = ('name',)
        
    def clean(self, *args, **kwargs):
        name = self.cleaned_data['name']
        defaultlist =['Draft','In Bound','Out Bound']
        if name:
            if name.title() in defaultlist :
                raise forms.ValidationError(
                    {'name': ["Name of folder should not be Draft, In Bound or Out Bound"]})
        return super(FolderForm, self).clean(*args, **kwargs)



class FileForm(forms.ModelForm):
    types = (
        ('Memo','Memo'),
        ('Application','Application'),
        ('Others','Others'),
    )
  
    type_of_document = forms.ChoiceField(choices = types,label=False)
    title = forms.CharField(label=False,required=True)
    document_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}),label=False,required=True)
    staff_through = forms.ModelChoiceField(label=False, queryset=User.objects.all(),required=False)
    supplier = forms.ModelChoiceField(label=False, queryset=Supplier.objects.all(),required=False)

    class Meta:
        model = DocumentCategory
        fields = ('type_of_document','title','document_date','staff_through')
        
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(FileForm,self).__init__(*args, **kwargs)
        self.fields['staff_through'].queryset = User.objects.filter(sub_division=self.request.user.sub_division)


            
class ParagraphForm(forms.ModelForm):
    paragraph = forms.CharField(
    widget=forms.Textarea(attrs={'maxlength': 1200}),
        label=False,)
   
    class Meta:
        model = DocumentDetails
        fields = ('paragraph',)

class CurrencyForm(forms.ModelForm):
    currency_id = forms.ModelChoiceField(label=False, queryset=Currency.objects.all(),required=True)
    class Meta:
        model = Document
        fields = ('currency_id',)

class BudgetForm(forms.ModelForm):
    item = forms.CharField(label=False,required=True)
    quantity = forms.IntegerField(label=False)
    amount = forms.FloatField(label=False) 
    
    class Meta:
        model = DocumentBudget
        fields = ('item','quantity','amount')
    

# class BudgetForm(forms.ModelForm):
#     name = forms.CharField(label=False,required=True)
#     file = forms.FileField(label=False,

#     amount = forms.FloatField(label=False) 
    
#     class Meta:
#         model = DocumentBudget
#         fields = ('name','quantity','amount')

class BudgetForm(forms.Form):
    name = forms.CharField(label=False,required=True)
    file = forms.FileField(label=False,required=True,help_text=('Supported formats: PDF'),
    validators=[validate_file_extension])
    amount = forms.FloatField(label=False,required=True)
    

    def clean_file(self):
        cleaned_data = super().clean()
        file = cleaned_data.get('file')

        if file:
            validate_file_extension(file)
        
        return file

class DocumentUploadFileForm(forms.Form):
    name = forms.CharField(label=False,required=True)
    file = forms.FileField(label=False,
    help_text=('Supported formats: PDF'),
    validators=[validate_file_extension])

    def clean_file(self):
        cleaned_data = super().clean()
        file = cleaned_data.get('file')

        if file:
            validate_file_extension(file)
        
        return file
    

class MinuteForm(forms.Form):
    name = forms.CharField(
           widget=forms.Textarea(attrs={'maxlength': 1200}),
           label=False,
    )


class ReturnForm(forms.Form):
    types = (
        
        ('Return Document For Correction','Return Document For Correction'),
        ('Cancel Document','Cancel Document'),
    )
    type_of_action = forms.ChoiceField(choices = types,label=False)
    name = forms.CharField(
           widget=forms.Textarea(attrs={'maxlength': 1200}),
           label=False,
    )

class ApprovedBudgetForm(forms.Form):
    
    amount = forms.FloatField(label=False) 
 