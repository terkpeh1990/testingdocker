from django import forms
from .models import *
from authentication.models import User

class DivisionForm(forms.ModelForm):
    name = forms.CharField(label=False)
    code = forms.CharField(label=False)
    tenant_id = forms.ModelChoiceField(label=False, queryset=Tenants.objects.all())
    class Meta:
        model = Devision
        fields = ('name','code','tenant_id',)

    def clean(self, *args, **kwargs):
        code = self.cleaned_data['code']
        code_exists = Devision.objects.filter(code=code)
        if code:
            if self.instance._state.adding and code_exists.exists():
                raise forms.ValidationError(
                    {'code': ["This Code Already Exist"]})
        return super(DivisionForm, self).clean(*args, **kwargs)
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(DivisionForm,self).__init__(*args, **kwargs)
        if self.request.user.is_superuser:
            self.fields['tenant_id'].queryset = Tenants.objects.filter()
        else:
            self.fields['tenant_id'].queryset = Tenants.objects.filter(name=self.request.user.devision.tenant_id.name)
        

class SubDivisionForm(forms.ModelForm):
    name = forms.CharField(label=False)
    code = forms.CharField(label=False)
    devision = forms.ModelChoiceField(
        queryset=Devision.objects.order_by('name'),label=False)
    class Meta:
        model = Sub_Devision
        fields = ('name','code','devision')

    def clean(self, *args, **kwargs):
        code = self.cleaned_data['code']
        code_exists = Devision.objects.filter(code=code)
        if code:
            if self.instance._state.adding and code_exists.exists():
                raise forms.ValidationError(
                    {'code': ["This Code Already Exist"]})
        return super(SubDivisionForm, self).clean(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(SubDivisionForm,self).__init__(*args, **kwargs)
        if self.request.user.is_superuser:
            self.fields['devision'].queryset = Devision.objects.filter()
        else:
            self.fields['devision'].queryset = Devision.objects.filter(name=self.request.user.devision.name)
        

class ApprovalForm(forms.ModelForm):
    sts= (
        ('Capital','Capital'),
        ('Consumables','Consumables'),
        ('All','All'),
         
    )
    st= (
        ('First','First'),
        ('Second','Second'),
        ('Third','Third'),
         
    )
   
    tenant_id = forms.ModelChoiceField(label=False, queryset=Tenants.objects.all(),required=False)
    user_id = forms.ModelChoiceField(label=False, queryset=User.objects.all())
    classification = forms.ChoiceField(choices = sts,label=False)
    type_of_approval = forms.ChoiceField(choices = st,label=False)
    class Meta:
        model = Approvals
        fields = ('tenant_id','user_id','classification','type_of_approval')
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(ApprovalForm,self).__init__(*args, **kwargs)
        if self.request.user.is_superuser:
            self.fields['tenant_id'].queryset = Tenants.objects.all()
            # self.fields['user_id'].queryset = User.objects.all()   
        else:
            self.fields['tenant_id'].queryset = Tenants.objects.filter(name=self.request.user.devision.tenant_id.name)
            self.fields['user_id'].queryset = User.objects.filter(tenant_id=self.request.user.devision.tenant_id.id)   


