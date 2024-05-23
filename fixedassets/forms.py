from django import forms
from .models import *
from django.forms.widgets import NumberInput
from company.models import Devision,Sub_Devision
from inventory.models import Brands,Products
from datetime import date
from authentication.models import User
from accounting.models import Fiscal_year


class ClassificationForm(forms.ModelForm):
    name = forms.CharField(label=False)
    class Meta:
        model = Classification
        fields = ('name',)

class AccountingRecognitionForm(forms.ModelForm):
    name = forms.CharField(label=False)
    classification =forms.ModelChoiceField(
        queryset=Classification.objects.all().order_by('name'),
        label=False,
        empty_label="Select One",
        required = True
    )
    class Meta:
        model = AccountingRecognition
        fields = ('name','classification')

class GFSCategoryForm(forms.ModelForm):
    code = forms.CharField(label=False,required=True)
    name = forms.CharField(label=False)
    class Meta:
        model = GFSCategory
        fields = ('code','name',)


class SubCategoryForm(forms.ModelForm):
    name = forms.CharField(label=False)
    ipsascategory = forms.ModelChoiceField(
        queryset=IPSASCategory.objects.all().order_by('name'),
        label=False,
        empty_label="Select One",
        required=True
    )
    class Meta:
        model = SubCategory
        fields = ('name','ipsascategory')

class IPSASCategoryForm(forms.ModelForm):
    name = forms.CharField(label=False)
    classification =forms.ModelChoiceField(
        queryset=Classification.objects.all().order_by('name'),
        label=False,
        empty_label="Select One",
        required=True
    )
    gfscategory =forms.ModelChoiceField(
        queryset=GFSCategory.objects.all().order_by('name'),
        label=False,
        empty_label="Select One",
        required=True
    )
    class Meta:
        model = IPSASCategory
        fields = ('name','classification','gfscategory')


class LocationForm(forms.ModelForm):
    code = forms.CharField(label=False)
    location = forms.CharField(label= False)
    class Meta:
        model = Location
        fields = ('code','location',)

class SourceOfFundingForm(forms.ModelForm):
    code = forms.CharField(label=False)
    funding = forms.CharField(label= False)
    class Meta:
        model = SourceOfFunding
        fields = ('code','funding',)

class MothodofAcquisitionForm(forms.ModelForm):
    name = forms.CharField(label=False)
    class Meta:
        model = MothodofAcquisition
        fields = ('name',)

class AssetsClassificationForm(forms.ModelForm):
    classification =forms.ModelChoiceField(
        queryset=Classification.objects.all().order_by('name'),
        label=False,
        empty_label="Select One",
        required=True
    )
    class Meta:
        model = FixedAsset
        fields = ('classification',)


class LandForm(forms.ModelForm):
    condition = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )
    usage = (
        ('Public Domain', 'Public Domain'),
        ('Private Domain', 'Private Domain'),
    )
    status = (
        ('In Use', 'In Use'),
        ('Not in Use', 'Not in Use'),
        ('Retired', 'Retired'),
        ('Disposed', 'Disposed'),
    )
    disposal = (
        ('Sales', 'Sales'),
        ('Auction', 'Auction'),
        ('Donated', 'Donated'),
        ('Trade-in/Exchanged', 'Trade-in/Exchanged'),
        ('Transfer-out to Other Govt Entities', 'Transfer-out to Other Govt Entities'),
        ('Scrapped', 'Scrapped'),
    )
    classification = forms.ModelChoiceField(
        queryset=Classification.objects.filter(name='Land').order_by('name'),
        label=False,
        empty_label="Select One",
        required=True
    )
    product = forms.ModelChoiceField(
        queryset=Products.objects.filter(type_of_product='Capital').order_by('name'),
        label=False,
        empty_label="Select One",
        required=True
    )

    description =forms.CharField(label=False,required=True)
    accountingrecognition = forms.ModelChoiceField(
        queryset=AccountingRecognition.objects.filter(classification__name='Land').order_by('name'),
        label=False,
        empty_label="Select One",
        required=True
    )
    amotization = forms.ChoiceField(label=False,choices=condition,required=True)
    usage =forms.ChoiceField(label=False,choices=usage,required=True)
    ipsascategory = forms.ModelChoiceField(
        queryset=IPSASCategory.objects.filter(classification__name='Land').order_by('name'),
        label=False,
        empty_label="Select One",
        required=True
    )
    subcategory = forms.ModelChoiceField(
        queryset=SubCategory.objects.all().order_by('name'),
        label=False,
        empty_label="Select One",
        required=True
    )
    size =forms.CharField(label=False,required=True)
    
    ghanapostgpsaddress=forms.CharField(label=False,required=True)
    titled = forms.ChoiceField(label=False,choices=condition,required=True)
    
    methodofacquisition =forms.ModelChoiceField(
        queryset=MothodofAcquisition.objects.all().order_by('name'),
        label=False,
        empty_label="Select One",
        required=True
    )
    currentstatus = forms.ChoiceField(label=False,choices=status,required=True)
    investmentproperty =forms.ChoiceField(label=False,choices=condition,required=True)
    fundsource =forms.ModelChoiceField(
        queryset=SourceOfFunding.objects.all().order_by('funding'),
        label=False,
        empty_label="Select One",
        required=True
    )
    value = forms.FloatField(label=False,required=False) 
    usefullife = forms.IntegerField(label=False,required=False)
    comments = forms.CharField(
    widget=forms.Textarea(attrs={'maxlength': 255}),
        label=False,required=True)

    class Meta:
        model = FixedAsset
        fields = ('classification','product','description','accountingrecognition','amotization','usage','ipsascategory','subcategory','size','ghanapostgpsaddress','titled',
                   'methodofacquisition','currentstatus','investmentproperty','fundsource','value','usefullife','comments')
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        instance = kwargs.get("instance")
        super(LandForm,self).__init__(*args, **kwargs)
        
        if instance:
            self.fields['subcategory'].queryset = SubCategory.objects.filter(ipsascategory=instance.ipsascategory)
        else:
            self.fields['subcategory'].queryset = SubCategory.objects.none()
        self.fields['product'].queryset = Products.objects.filter(tenant_id= self.request.user.devision.tenant_id,type_of_product='Capital')

        if 'ipsascategory' in self.data:
            try:
                ipsascategory = int(self.data.get('ipsascategory'))
                self.fields['subcategory'].queryset = SubCategory.objects.filter(
                    ipsascategory=ipsascategory)
            except (ValueError, TypeError):
                pass


class BuildingForm(forms.ModelForm):
    condition = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )
    usagetype = (
        ('Pool', 'Pool'),
        ('Assigned', 'Assigned'),
    )
    
    status = (
        ('In Use', 'In Use'),
        ('Not in Use', 'Not in Use'),
        ('Retired', 'Retired'),
        ('Disposed', 'Disposed'),
    )
    disposal = (
        ('Sales', 'Sales'),
        ('Auction', 'Auction'),
        ('Donated', 'Donated'),
        ('Trade-in/Exchanged', 'Trade-in/Exchanged'),
        ('Transfer-out to Other Govt Entities', 'Transfer-out to Other Govt Entities'),
        ('Scrapped', 'Scrapped'),
    )
    bcondition=(
        ('Good','Good'),
        ('Needs Repair/Renovation/Servicing','Needs Repair/Renovation/Servicing'),
        ('Irrepairable/Unserviceable','Irrepairable/Unserviceable'),
        ('Not Sighted','Not Sighted'),
    )
    classification = forms.ModelChoiceField(
        queryset=Classification.objects.filter(name='Buldings And Other Structures').order_by('name'),
        label=False,
        empty_label="Select One",
        required=True
    )
    product = forms.ModelChoiceField(
        queryset=Products.objects.filter(type_of_product='Capital').order_by('name'),
        label=False,
        empty_label="Select One",
        required=True
    )
    description =forms.CharField(label=False,required=True)
    accountingrecognition = forms.ModelChoiceField(
        queryset=AccountingRecognition.objects.filter(classification__name='Buldings And Other Structures').order_by('name'),
        label=False,
        empty_label="Select One",
        required=True
    )
    depreciation = forms.ChoiceField(label=False,choices=condition,required=True)
    ipsascategory = forms.ModelChoiceField(
        queryset=IPSASCategory.objects.filter(classification__name='Buldings And Other Structures').order_by('name'),
        label=False,
        empty_label="Select One",
        required=True
    )
    subcategory = forms.ModelChoiceField(
        queryset=SubCategory.objects.all().order_by('name'),
        label=False,
        empty_label="Select One",
        required=True
    )
    quantity=forms.IntegerField(label=False,required=False)
    ghanapostgpsaddress=forms.CharField(label=False,required=True)
    dateplacedinservice=forms.DateField(widget=NumberInput(attrs={'type': 'date'}),label=False)
    methodofacquisition =forms.ModelChoiceField(
        queryset=MothodofAcquisition.objects.all().order_by('name'),
        label=False,
        empty_label="Select One",
        required=True
    )
   
    conditions = forms.ChoiceField(label=False,choices=bcondition,required=True)
    investmentproperty =forms.ChoiceField(label=False,choices=condition,required=True)
    fundsource =forms.ModelChoiceField(
        queryset=SourceOfFunding.objects.all().order_by('funding'),
        label=False,
        empty_label="Select One",
        required=True
    )
    value = forms.FloatField(label=False,required=False) 
    usefullife = forms.IntegerField(label=False,required=False)
    comments = forms.CharField(
    widget=forms.Textarea(attrs={'maxlength': 255}),
        label=False,required=True)

    class Meta:
        model = FixedAsset
        fields = ('classification','product','description','accountingrecognition','depreciation','ipsascategory','subcategory','quantity','ghanapostgpsaddress','dateplacedinservice',
        'methodofacquisition','conditions','investmentproperty','fundsource','value','usefullife','comments')
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        instance = kwargs.get("instance")
        super(BuildingForm,self).__init__(*args, **kwargs)
       
        if instance:
            
            self.fields['subcategory'].queryset = SubCategory.objects.filter(ipsascategory=instance.ipsascategory)
        else:
            
            self.fields['subcategory'].queryset = SubCategory.objects.none()
        self.fields['product'].queryset = Products.objects.filter(tenant_id= self.request.user.devision.tenant_id,type_of_product='Capital')
        if 'ipsascategory' in self.data:
            try:
                ipsascategory = int(self.data.get('ipsascategory'))
                self.fields['subcategory'].queryset = SubCategory.objects.filter(
                    ipsascategory=ipsascategory)
            except (ValueError, TypeError):
                pass

class TransportForm(forms.ModelForm):
    years = [(year, str(year)) for year in range(1700, date.today().year + 1)]
    condition = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )
    usagetype = (
        ('Pool', 'Pool'),
        ('Assigned', 'Assigned'),
    )
    
    status = (
        ('In Use', 'In Use'),
        ('Not in Use', 'Not in Use'),
        ('Retired', 'Retired'),
        ('Disposed', 'Disposed'),
    )
    disposal = (
        ('Sales', 'Sales'),
        ('Auction', 'Auction'),
        ('Donated', 'Donated'),
        ('Trade-in/Exchanged', 'Trade-in/Exchanged'),
        ('Transfer-out to Other Govt Entities', 'Transfer-out to Other Govt Entities'),
        ('Scrapped', 'Scrapped'),
    )
    bcondition=(
        ('Good','Good'),
        ('Needs Repair/Renovation/Servicing','Needs Repair/Renovation/Servicing'),
        ('Irrepairable/Unserviceable','Irrepairable/Unserviceable'),
        ('Not Sighted','Not Sighted'),
    )
    classification = forms.ModelChoiceField(
        queryset=Classification.objects.filter(name='Transport Equipments').order_by('name'),
        label=False,
        empty_label="Select One",
        required=True
    )
    product = forms.ModelChoiceField(
        queryset=Products.objects.filter(type_of_product='Capital').order_by('name'),
        label=False,
        empty_label="Select One",
        required=True
    )
    description =forms.CharField(label=False,required=True)
    registrationnumber =forms.CharField(label=False,required=True)
    accountingrecognition = forms.ModelChoiceField(
        queryset=AccountingRecognition.objects.filter(classification__name='Transport Equipments').order_by('name'),
        label=False,
        empty_label="Select One",
        required=True
    )
    depreciation = forms.ChoiceField(label=False,choices=condition,required=True)
    ipsascategory = forms.ModelChoiceField(
        queryset=IPSASCategory.objects.filter(classification__name='Transport Equipments').order_by('name'),
        label=False,
        empty_label="Select One",
        required=True
    )
    subcategory = forms.ModelChoiceField(
        queryset=SubCategory.objects.all().order_by('name'),
        label=False,
        empty_label="Select One",
        required=True
    )
    quantity=forms.IntegerField(label=False,required=False)
    
    dateplacedinservice=forms.DateField(widget=NumberInput(attrs={'type': 'date'}),label=False)
    colour =forms.CharField(label=False,required=True)
    chassisno =forms.CharField(label=False,required=True)
    engineserialno =forms.CharField(label=False,required=True)
    manufacturer = forms.ModelChoiceField(
        queryset=Brands.objects.all().order_by('name'),
        label=False,
        empty_label="Select One",
        required=True
    )
    model = forms.CharField(label=False,required=True)
    modelyear =forms.ChoiceField(choices=years, initial=date.today().year,label=False,required=True)
    
    methodofacquisition =forms.ModelChoiceField(
        queryset=MothodofAcquisition.objects.all().order_by('name'),
        label=False,
        empty_label="Select One",
        required=True
    )
    conditions = forms.ChoiceField(label=False,choices=bcondition,required=True)
    investmentproperty =forms.ChoiceField(label=False,choices=condition,required=True)
    fundsource =forms.ModelChoiceField(
        queryset=SourceOfFunding.objects.all().order_by('funding'),
        label=False,
        empty_label="Select One",
        required=True
    )
    value = forms.FloatField(label=False,required=False) 
    usefullife = forms.IntegerField(label=False,required=False)
    comments = forms.CharField(
    widget=forms.Textarea(attrs={'maxlength': 255}),
        label=False,required=True)

    class Meta:
        model = FixedAsset
        fields = ('classification','product','description','registrationnumber','accountingrecognition','depreciation','ipsascategory','subcategory','quantity','dateplacedinservice',
        'colour','chassisno','engineserialno','manufacturer','model','modelyear','methodofacquisition',
        'conditions','investmentproperty','fundsource','value','usefullife','comments')
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        instance = kwargs.get("instance")
        super(TransportForm,self).__init__(*args, **kwargs)
       
        if instance:
            
            self.fields['subcategory'].queryset = SubCategory.objects.filter(ipsascategory=instance.ipsascategory)
        else:
            
            self.fields['subcategory'].queryset = SubCategory.objects.none()
        self.fields['product'].queryset = Products.objects.filter(tenant_id= self.request.user.devision.tenant_id,type_of_product='Capital')
        self.fields['manufacturer'].queryset = Brands.objects.filter(tenant_id= self.request.user.devision.tenant_id)
        if 'ipsascategory' in self.data:
            try:
                ipsascategory = int(self.data.get('ipsascategory'))
                self.fields['subcategory'].queryset = SubCategory.objects.filter(
                    ipsascategory=ipsascategory)
            except (ValueError, TypeError):
                pass


class OutdoorForm(forms.ModelForm):
    years = [(year, str(year)) for year in range(1700, date.today().year + 1)]
    condition = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )
    usagetype = (
        ('Pool', 'Pool'),
        ('Assigned', 'Assigned'),
    )
    
    status = (
        ('In Use', 'In Use'),
        ('Not in Use', 'Not in Use'),
        ('Retired', 'Retired'),
        ('Disposed', 'Disposed'),
    )
    disposal = (
        ('Sales', 'Sales'),
        ('Auction', 'Auction'),
        ('Donated', 'Donated'),
        ('Trade-in/Exchanged', 'Trade-in/Exchanged'),
        ('Transfer-out to Other Govt Entities', 'Transfer-out to Other Govt Entities'),
        ('Scrapped', 'Scrapped'),
    )
    bcondition=(
        ('Good','Good'),
        ('Needs Repair/Renovation/Servicing','Needs Repair/Renovation/Servicing'),
        ('Irrepairable/Unserviceable','Irrepairable/Unserviceable'),
        ('Not Sighted','Not Sighted'),
    )
    classification = forms.ModelChoiceField(
        queryset=Classification.objects.filter(name='Outdoor Machinery And Equipments').order_by('name'),
        label=False,
        empty_label="Select One",
        required=True
    )
    product = forms.ModelChoiceField(
        queryset=Products.objects.filter(type_of_product='Capital').order_by('name'),
        label=False,
        empty_label="Select One",
        required=True
    )
    description =forms.CharField(label=False,required=True)
    accountingrecognition = forms.ModelChoiceField(
        queryset=AccountingRecognition.objects.filter(classification__name='Outdoor Machinery And Equipments').order_by('name'),
        label=False,
        empty_label="Select One",
        required=True
    )
    depreciation = forms.ChoiceField(label=False,choices=condition,required=True)
    ipsascategory = forms.ModelChoiceField(
        queryset=IPSASCategory.objects.filter(classification__name='Outdoor Machinery And Equipments').order_by('name'),
        label=False,
        empty_label="Select One",
        required=True
    )
    subcategory = forms.ModelChoiceField(
        queryset=SubCategory.objects.all().order_by('name'),
        label=False,
        empty_label="Select One",
        required=True
    )
    quantity=forms.IntegerField(label=False,required=False)
    ghanapostgpsaddress = forms.CharField(label=False)
    dateplacedinservice=forms.DateField(widget=NumberInput(attrs={'type': 'date'}),label=False)
    chassisno =forms.CharField(label=False,required=True)
    engineserialno =forms.CharField(label=False)
    manufacturer = forms.ModelChoiceField(
        queryset=Brands.objects.all().order_by('name'),
        label=False,
        empty_label="Select One",
    )
    model = forms.CharField(label=False,required=True)
    modelyear =forms.ChoiceField(choices=years, initial=date.today().year,label=False)
    tagno = forms.CharField(label=False,required=True)
    
    methodofacquisition =forms.ModelChoiceField(
        queryset=MothodofAcquisition.objects.all().order_by('name'),
        label=False,
        empty_label="Select One",
        required=True
    )
    conditions = forms.ChoiceField(label=False,choices=bcondition,required=True)
    investmentproperty =forms.ChoiceField(label=False,choices=condition,required=True)
    fundsource =forms.ModelChoiceField(
        queryset=SourceOfFunding.objects.all().order_by('funding'),
        label=False,
        empty_label="Select One",
        required=True
    )
    value = forms.FloatField(label=False,required=False) 
    usefullife = forms.IntegerField(label=False,required=False)
    comments = forms.CharField(
    widget=forms.Textarea(attrs={'maxlength': 255}),
        label=False,required=True)

    class Meta:
        model = FixedAsset
        fields = ('classification','product','description','accountingrecognition','depreciation','ipsascategory','subcategory','quantity','ghanapostgpsaddress','dateplacedinservice',
        'chassisno','engineserialno','manufacturer','model','modelyear','tagno','methodofacquisition','conditions','investmentproperty','fundsource','value','usefullife','comments')
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        instance = kwargs.get("instance")
        super(OutdoorForm,self).__init__(*args, **kwargs)
        
        if instance:
            
            self.fields['subcategory'].queryset = SubCategory.objects.filter(ipsascategory=instance.ipsascategory)
        else:
            self.fields['subcategory'].queryset = SubCategory.objects.none()
        self.fields['product'].queryset = Products.objects.filter(tenant_id= self.request.user.devision.tenant_id,type_of_product='Capital')
        self.fields['manufacturer'].queryset = Brands.objects.filter(tenant_id= self.request.user.devision.tenant_id)
        if 'ipsascategory' in self.data:
            try:
                ipsascategory = int(self.data.get('ipsascategory'))
                self.fields['subcategory'].queryset = SubCategory.objects.filter(
                    ipsascategory=ipsascategory)
            except (ValueError, TypeError):
                pass


class IndoorForm(forms.ModelForm):
    years = [(year, str(year)) for year in range(1700, date.today().year + 1)]
    condition = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )
    usagetype = (
        ('Pool', 'Pool'),
        ('Assigned', 'Assigned'),
    )
    
    status = (
        ('In Use', 'In Use'),
        ('Not in Use', 'Not in Use'),
        ('Retired', 'Retired'),
        ('Disposed', 'Disposed'),
    )
    disposal = (
        ('Sales', 'Sales'),
        ('Auction', 'Auction'),
        ('Donated', 'Donated'),
        ('Trade-in/Exchanged', 'Trade-in/Exchanged'),
        ('Transfer-out to Other Govt Entities', 'Transfer-out to Other Govt Entities'),
        ('Scrapped', 'Scrapped'),
    )
    bcondition=(
        ('Good','Good'),
        ('Needs Repair/Renovation/Servicing','Needs Repair/Renovation/Servicing'),
        ('Irrepairable/Unserviceable','Irrepairable/Unserviceable'),
        ('Not Sighted','Not Sighted'),
    )
    classification = forms.ModelChoiceField(
        queryset=Classification.objects.filter(name='Indoor').order_by('name'),
        label=False,
        empty_label="Select One",
        required=True
    )
    product = forms.ModelChoiceField(
        queryset=Products.objects.filter(type_of_product='Capital').order_by('name'),
        label=False,
        empty_label="Select One",
        required=True
    )
    description =forms.CharField(label=False,required=True)
    accountingrecognition = forms.ModelChoiceField(
        queryset=AccountingRecognition.objects.filter(classification__name='Indoor').order_by('name'),
        label=False,
        empty_label="Select One",
        required=True
    )
    depreciation = forms.ChoiceField(label=False,choices=condition,required=True)
    ipsascategory = forms.ModelChoiceField(
        queryset=IPSASCategory.objects.filter(classification__name='Indoor').order_by('name'),
        label=False,
        empty_label="Select One",
        required=True
    )
    subcategory = forms.ModelChoiceField(
        queryset=SubCategory.objects.all().order_by('name'),
        label=False,
        empty_label="Select One",
        required=True
    )
    quantity=forms.IntegerField(label=False,required=False)
    
    
    dateplacedinservice=forms.DateField(widget=NumberInput(attrs={'type': 'date'}),label=False)
    chassisno =forms.CharField(label=False,required=True)
    manufacturer = forms.ModelChoiceField(
        queryset=Brands.objects.all().order_by('name'),
        label=False,
        empty_label="Select One",
    )
    
    tagno = forms.CharField(label=False,required=True)
   
    methodofacquisition =forms.ModelChoiceField(
        queryset=MothodofAcquisition.objects.all().order_by('name'),
        label=False,
        empty_label="Select One",
        required=True
    )
    conditions = forms.ChoiceField(label=False,choices=bcondition,required=True)
    investmentproperty = forms.ChoiceField(label=False,choices=condition,required=True)
    fundsource =forms.ModelChoiceField(
        queryset=SourceOfFunding.objects.all().order_by('funding'),
        label=False,
        empty_label="Select One",
        required=True
    )
    value = forms.FloatField(label=False,required=False) 
    usefullife = forms.IntegerField(label=False,required=False)
    comments = forms.CharField(
    widget=forms.Textarea(attrs={'maxlength': 255}),
        label=False,required=True)

    class Meta:
        model = FixedAsset
        fields = ('classification','product','description','accountingrecognition','depreciation','ipsascategory','subcategory','quantity','dateplacedinservice',
        'chassisno','manufacturer','tagno','methodofacquisition','conditions','investmentproperty','fundsource','value','usefullife','comments')
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        instance = kwargs.get("instance")
        super(IndoorForm,self).__init__(*args, **kwargs)
        
        if instance:
            
            self.fields['subcategory'].queryset = SubCategory.objects.filter(ipsascategory=instance.ipsascategory)
        else:
           
            self.fields['subcategory'].queryset = SubCategory.objects.none()
        self.fields['manufacturer'].queryset = Brands.objects.filter(tenant_id= self.request.user.devision.tenant_id)
        self.fields['product'].queryset = Products.objects.filter(tenant_id= self.request.user.devision.tenant_id,type_of_product='Capital')
        if 'ipsascategory' in self.data:
            try:
                ipsascategory = int(self.data.get('ipsascategory'))
                self.fields['subcategory'].queryset = SubCategory.objects.filter(
                    ipsascategory=ipsascategory)
            except (ValueError, TypeError):
                pass


class WIPForm(forms.ModelForm):
    years = [(year, str(year)) for year in range(1700, date.today().year + 1)]
    accountingstatus = (
        ('In-progress','In-progress'),
        ('Completed','Completed'),
        ('Completed and Transferred','Completed and Transferred'),
       
    )
    condition = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )
    usagetype = (
        ('Pool', 'Pool'),
        ('Assigned', 'Assigned'),
    )
    
    status = (
        ('In Use', 'In Use'),
        ('Not in Use', 'Not in Use'),
        ('Retired', 'Retired'),
        ('Disposed', 'Disposed'),
        ('On-going', 'On-going'),
        ('Abandoned', 'Abandoned'),
        ('Suspended', 'Suspended'),
    )
    disposal = (
        ('Sales', 'Sales'),
        ('Auction', 'Auction'),
        ('Donated', 'Donated'),
        ('Trade-in/Exchanged', 'Trade-in/Exchanged'),
        ('Transfer-out to Other Govt Entities', 'Transfer-out to Other Govt Entities'),
        ('Scrapped', 'Scrapped'),
    )
    bcondition=(
        ('Good','Good'),
        ('Needs Repair/Renovation/Servicing','Needs Repair/Renovation/Servicing'),
        ('Irrepairable/Unserviceable','Irrepairable/Unserviceable'),
        ('Not Sighted','Not Sighted'),
    )
    classification = forms.ModelChoiceField(
        queryset=Classification.objects.filter(name='Wip Or Cip').order_by('name'),
        label=False,
        empty_label="Select One",
        required=True
    )
    product = forms.ModelChoiceField(
        queryset=Products.objects.filter(type_of_product='Capital').order_by('name'),
        label=False,
        empty_label="Select One",
        required=True
    )
    description =forms.CharField(label=False,required=True)
    accountingrecognition = forms.ModelChoiceField(
        queryset=AccountingRecognition.objects.filter(classification__name='Wip Or Cip').order_by('name'),
        label=False,
        empty_label="Select One",
        required=True
    )
    depreciation = forms.ChoiceField(label=False,choices=condition,required=True)
    ipsascategory = forms.ModelChoiceField(
        queryset=IPSASCategory.objects.filter(classification__name='Wip Or Cip').order_by('name'),
        label=False,
        empty_label="Select One",
        required=True
    )
    quantity=forms.IntegerField(label=False,required=False)
    
    ghanapostgpsaddress = forms.CharField(label=False)
    commencement_date=forms.DateField(widget=NumberInput(attrs={'type': 'date'}),label=False)
    expectedcompletion_date=forms.DateField(widget=NumberInput(attrs={'type': 'date'}),label=False)
    
    accountingstatus = forms.ChoiceField(label=False,choices=accountingstatus,required=True)
    methodofacquisition =forms.ModelChoiceField(
        queryset=MothodofAcquisition.objects.all().order_by('name'),
        label=False,
        empty_label="Select One",
        required=True
    )
    
    fundsource =forms.ModelChoiceField(
        queryset=SourceOfFunding.objects.all().order_by('funding'),
        label=False,
        empty_label="Select One",
        required=True
    )
    costbf = forms.FloatField(label=False,required=False) 
    currentperiodcost = forms.FloatField(label=False,required=False) 
    costcf = forms.FloatField(label=False,required=False) 
    comments = forms.CharField(
    widget=forms.Textarea(attrs={'maxlength': 255}),
        label=False,required=True)

    class Meta:
        model = FixedAsset
        fields = ('classification','product','description','accountingrecognition','depreciation','ipsascategory','quantity','ghanapostgpsaddress','commencement_date',
        'expectedcompletion_date','accountingstatus','methodofacquisition','fundsource','costbf','currentperiodcost','costcf','comments')
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        instance = kwargs.get("instance")
        
        super(WIPForm,self).__init__(*args, **kwargs)

        self.fields['product'].queryset = Products.objects.filter(tenant_id= self.request.user.devision.tenant_id,type_of_product='Capital')

        
        
class AssetsAssignmentForm(forms.ModelForm):
    usagetype = (
            ('Pool', 'Pool'),
            ('Assigned', 'Assigned'),
        )
       
    costcenter = forms.ModelChoiceField(
        queryset=Devision.objects.all().order_by('name'),
        label=False,
        empty_label="Select One",
        required=True
    )
    subcostcenter =forms.ModelChoiceField(
        queryset=Sub_Devision.objects.all(),
        label=False,
        empty_label="Select One",
        required=True
    )
    usagetype= forms.ChoiceField(label=False,choices=usagetype,required=True)
    
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label=False,
        empty_label="Select One",
        required=True
    )
    assigndate=forms.DateField(widget=NumberInput(attrs={'type': 'date'}),label=False)
    class Meta:
        model = FixedAssetsAssignment
        fields = ('costcenter','subcostcenter','usagetype','user','assigndate')
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        instance = kwargs.get("instance")
        super(AssetsAssignmentForm,self).__init__(*args, **kwargs)
        if self.request.user.is_superuser:
            self.fields['costcenter'].queryset = Devision.objects.filter(status = True)
            
        else:
            self.fields['costcenter'].queryset = Devision.objects.filter(tenant_id=self.request.user.devision.tenant_id.id,status = True)
           
        if instance:
            self.fields['subcostcenter'].queryset = Sub_Devision.objects.filter(devision=instance.costcenter)
            self.fields['user'].queryset = User.objects.filter(sub_division=instance.subcostcenter)
        else:
            self.fields['subcostcenter'].queryset = Sub_Devision.objects.none()
            self.fields['user'].queryset = User.objects.none()


        if 'costcenter' in self.data:
            try:
                devision = int(self.data.get('costcenter'))
                self.fields['subcostcenter'].queryset = Sub_Devision.objects.filter(
                    devision=devision)
            except (ValueError, TypeError):
                pass
        
        if 'subcostcenter' in self.data:
            try:
                subcostcenter = int(self.data.get('subcostcenter'))
                self.fields['user'].queryset = User.objects.filter(
                    sub_division=subcostcenter)
            except (ValueError, TypeError):
                pass

    def clean_usage_type(self, *args, **kwargs):
        name = self.cleaned_data['usagetype'].title()
        user = self.cleaned_data['user']
        if  user is None:
            raise forms.ValidationError(
                {'user': ["Please Select a Staff"]})
        
        return super(AssetsAssignmentForm, self).clean(*args, **kwargs)

class AssetsReturnedForm(forms.ModelForm):
    
    returndate=forms.DateField(widget=NumberInput(attrs={'type': 'date'}),label=False,required=True)
    class Meta:
        model = FixedAssetsAssignment
        fields = ('returndate',)
    
    

    def clean_returndate_type(self, *args, **kwargs):
        returndate = self.cleaned_data['returndate'].title()
       
        if  returndate is None:
            raise forms.ValidationError(
                {'returndate': ["Please Select a Date"]})
        
        return super(AssetsAssignmentForm, self).clean(*args, **kwargs)

class DepreciationForm(forms.ModelForm):
    """Form definition for MODELNAME."""
    accountingyear = forms.ModelChoiceField(
        queryset=Fiscal_year.objects.all().order_by('-period'),
        label=False,
        empty_label="Select One",
        required=True
    )

    class Meta:
        """Meta definition for MODELNAMEform."""

        model = Depreciation
        fields = ('accountingyear',)

class ReevaluationForm(forms.ModelForm):
    """Form definition for MODELNAME."""
    accountingyear = forms.ModelChoiceField(
        queryset=Fiscal_year.objects.all().order_by('-period'),
        label=False,
        empty_label="Select One",
        required=True
    )
    newvalue =forms.FloatField(label=False,required=True) 
    usefullife =forms.IntegerField(label=False,required=False)

    class Meta:
        """Meta definition for MODELNAMEform."""

        model = Reevaluation
        fields = ('accountingyear','newvalue','usefullife')

class DesposalForm(forms.ModelForm):
    """Form definition for MODELNAME."""
    disposal = (
        ('Sales', 'Sales'),
        ('Auction', 'Auction'),
        ('Donated', 'Donated'),
        ('Trade-in/Exchanged', 'Trade-in/Exchanged'),
        ('Transfer-out to Other Govt Entities', 'Transfer-out to Other Govt Entities'),
        ('Scrapped', 'Scrapped'),
    )
    accountingyear = forms.ModelChoiceField(
        queryset=Fiscal_year.objects.all().order_by('-period'),
        label=False,
        empty_label="Select One",
        required=True
    )
    desposal_date =forms.DateField(widget=NumberInput(attrs={'type': 'date'}),label=False,required=True)
    methodofdesposal =forms.ChoiceField(label=False,choices=disposal,required=True)
    proceedsfromsales= forms.FloatField(label=False,required=True)

    class Meta:
        """Meta definition for MODELNAMEform."""

        model = Disposals
        fields = ('accountingyear','desposal_date','methodofdesposal','proceedsfromsales')