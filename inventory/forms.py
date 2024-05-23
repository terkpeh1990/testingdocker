from django import forms
from .models import *
from django.forms.widgets import NumberInput
from company.models import *
from purchase_order.models import LocalPurchasingOrder
from fixedassets.models import *
from datetime import date
from fixedassets.models import FixedAsset

class CategoryForm(forms.ModelForm):
    name = forms.CharField(label=False)
    tenant_id = forms.ModelChoiceField(label=False, queryset=Tenants.objects.all(),required=False)
    class Meta:
        model = Categorys
        fields = ('name','tenant_id')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(CategoryForm,self).__init__(*args, **kwargs)
        if self.request.user.is_superuser:
            self.fields['tenant_id'].queryset = Tenants.objects.all()
        else:
            self.fields['tenant_id'].queryset = Tenants.objects.filter(name=self.request.user.devision.tenant_id.name)

class BrandForm(forms.ModelForm):
    name = forms.CharField(label=False)
    tenant_id = forms.ModelChoiceField(label=False, queryset=Tenants.objects.all(),required=False)
    class Meta:
        model = Brands
        fields = ('name','tenant_id')
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(BrandForm,self).__init__(*args, **kwargs)
        if self.request.user.is_superuser:
            self.fields['tenant_id'].queryset = Tenants.objects.filter()
        else:
            self.fields['tenant_id'].queryset = Tenants.objects.filter(name=self.request.user.devision.tenant_id.name)

class MeasurementForm(forms.ModelForm):
    name = forms.CharField(label=False)
    tenant_id = forms.ModelChoiceField(label=False, queryset=Tenants.objects.all(),required=False)
    class Meta:
        model = Unit_of_Measurement
        fields = ('name','tenant_id')
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(MeasurementForm,self).__init__(*args, **kwargs)
        if self.request.user.is_superuser:
            self.fields['tenant_id'].queryset = Tenants.objects.filter()
        else:
            self.fields['tenant_id'].queryset = Tenants.objects.filter(name=self.request.user.devision.tenant_id.name)


class ProductForm(forms.ModelForm):
    sts= (
        ('Capital','Capital'),
        ('Consumables','Consumables'),
         
    )
    # brand_id =forms.ModelChoiceField(queryset=Brands.objects.all().order_by('name'),label=False,required=False)
    category_id =forms.ModelChoiceField(queryset=Categorys.objects.all().order_by('name'),label=False)
    name = forms.CharField(label=False)
    restock_level = forms.IntegerField(label=False)
    unit_of_measurement =forms.ModelChoiceField(queryset=Unit_of_Measurement.objects.order_by('name'),label=False)
    tenant_id = forms.ModelChoiceField(label=False, queryset=Tenants.objects.all(),required=False)
    type_of_product= forms.ChoiceField(label=False,choices= sts)
    class Meta:
        model = Products
        fields = ('category_id','name','restock_level','unit_of_measurement','type_of_product','tenant_id')
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(ProductForm,self).__init__(*args, **kwargs)
        if self.request.user.is_superuser:
            self.fields['tenant_id'].queryset = Tenants.objects.filter()
        else:
            self.fields['tenant_id'].queryset = Tenants.objects.filter(name=self.request.user.devision.tenant_id.name)
            self.fields['category_id'].queryset = Categorys.objects.filter(tenant_id=self.request.user.devision.tenant_id)
            self.fields['unit_of_measurement'].queryset = Unit_of_Measurement.objects.filter(tenant_id=self.request.user.devision.tenant_id)
            # self.fields['brand_id'].queryset = Brands.objects.filter(tenant_id=self.request.user.devision.tenant_id)


    def clean_name(self):
        return self.cleaned_data['name'].title()

    def clean_name_avialable(self, *args, **kwargs):
        name = self.cleaned_data['name'].title()
        name_exists = Products.objects.filter(name=name)
        if name:
            if name_exists.exists():
                raise forms.ValidationError(
                    {'name': ["A product with this name already exist"]})
        
        return super(ProductForm, self).clean(*args, **kwargs)

class SupplierForm(forms.ModelForm):
    name = forms.CharField(label=False)
    address = forms.CharField(label=False)
    city = forms.CharField(label=False)
    country = forms.CharField(label=False)
    phone_number = forms.CharField(label=False)
    supplier_email = forms.CharField(label=False)
    
    tenant_id = forms.ModelChoiceField(label=False, queryset=Tenants.objects.all(),required=False)
    class Meta:
        model = Supplier
        fields = ('name','address','city','country','phone_number','supplier_email','tenant_id')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(SupplierForm,self).__init__(*args, **kwargs)
        if self.request.user.is_superuser:
            self.fields['tenant_id'].queryset = Tenants.objects.all()
        else:
            self.fields['tenant_id'].queryset = Tenants.objects.filter(name=self.request.user.devision.tenant_id.name)



class RestockForm(forms.ModelForm):
   
    restock_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}),label=False)
    supplier_id = forms.ModelChoiceField(label=False, queryset=Supplier.objects.all())
    driver_name = forms.CharField(label=False)
    driver_contact = forms.CharField(label=False)
    note = forms.CharField(
    widget=forms.Textarea(attrs={'maxlength': 1200}),
        label=False,required=True)
    tenant_id = forms.ModelChoiceField(label=False, queryset=Tenants.objects.all(),required=False)

    class Meta:
        model = Restocks
        fields = ('restock_date','supplier_id','driver_name','driver_contact','note','tenant_id')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(RestockForm,self).__init__(*args, **kwargs)
        if self.request.user.is_superuser:
            self.fields['tenant_id'].queryset = Tenants.objects.all()
            self.fields['supplier_id'].queryset = Supplier.objects.all()
        else:
            self.fields['tenant_id'].queryset = Tenants.objects.filter(name=self.request.user.devision.tenant_id.name)
            self.fields['supplier_id'].queryset = Supplier.objects.filter(tenant_id=self.request.user.devision.tenant_id.id)
            

    def clean_driver_name(self):
        return self.cleaned_data['driver_name'].title()
  

class RestockDetailForm(forms.ModelForm):
   
    quantity = forms.IntegerField(label=False)
    expiring_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}),label=False)

    class Meta:
        model = Restock_details
        fields = ('quantity','expiring_date',)


class JobForm(forms.ModelForm):
    certification_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}),label=False)
    supplier_id = forms.ModelChoiceField(label=False, queryset=Supplier.objects.all())
    classification = forms.ModelChoiceField(
        queryset=Classification.objects.all().order_by('name'),
        label=False,
        empty_label="Select One",
        required=True
    )
    category = forms.ModelChoiceField(
        queryset=Categorys.objects.all().order_by('name'),
        label=False,
        empty_label="Select One",
        required=True)
    product = forms.ModelChoiceField(
        queryset=Products.objects.all().order_by('name'),
        label=False,
        empty_label="Select One",
        required=True)
    description = forms.CharField(label=False,required=True)
    note = forms.CharField(
    widget=forms.Textarea(attrs={'maxlength': 1200}),
        label=False,required=True)
    sra = forms.CharField(label=False)
    tenant_id = forms.ModelChoiceField(label=False, queryset=Tenants.objects.all(),required=False)
    class Meta:
        model = Job_Certification
        fields = ('certification_date','supplier_id','classification','category','product','description','note','sra','tenant_id')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        instance = kwargs.get("instance")
        super(JobForm,self).__init__(*args, **kwargs)
        if instance:
            if self.request.user.is_superuser:
                self.fields['tenant_id'].queryset = Tenants.objects.all()
                self.fields['supplier_id'].queryset = Supplier.objects.all()
            else:
                self.fields['tenant_id'].queryset = Tenants.objects.filter(name=self.request.user.devision.tenant_id.name)
                self.fields['supplier_id'].queryset = Supplier.objects.filter(tenant_id=self.request.user.devision.tenant_id.id)
            self.fields['product'].queryset = Products.objects.filter(category_id=instance.category)
        else:
            self.fields['product'].queryset = Products.objects.none()
            self.fields['supplier_id'].queryset = Supplier.objects.filter(tenant_id=self.request.user.devision.tenant_id.id)
        self.fields['category'].queryset = Categorys.objects.filter(tenant_id=self.request.user.devision.tenant_id.id).order_by('name')
        
        if 'category' in self.data:
            try:
                category = int(self.data.get('category'))
                self.fields['product'].queryset = Products.objects.filter(category_id=category)
            except (ValueError, TypeError):
                pass



    def clean_driver_name(self):
        return self.cleaned_data['driver_name'].title()
    


# class JobDetailForm(forms.ModelForm):
#     status = (
#         ('Accepted', 'Accepted'),
#         ('Rejected', 'Rejected'),
       
#     )  
#     funding = (
#         ('Internal', 'Internal'),
#         ('Donor', 'Donor'),
       
#     )
#     brand_id = forms.ModelChoiceField(label=False, queryset=Brands.objects.all())
#     serial_number = forms.CharField(label=False)
#     description = forms.CharField(label=False)
#     status= forms.ChoiceField(choices = status,label=False)
#     funding = forms.ChoiceField(choices = funding,label=False)
#     class Meta:
#         model = Job_detail
#         fields = ('serial_number','description','status','funding')

#     def __init__(self, *args, **kwargs):
#         self.request = kwargs.pop("request")
#         super(JobDetailForm, self).__init__(*args, **kwargs)
#         self.fields['serial_number'].widget.attrs.update({'autofocus': 'autofocus'})
        
#         if self.request.user.is_superuser:
#             self.fields['brand_id'].queryset = Brands.objects.all() 
#         else:
#             self.fields['brand_id'].queryset = Brands.objects.filter(tenant_id=self.request.user.devision.tenant_id) 
            
#     def describtion(self):
#         return self.cleaned_data['description'].title()

class JobLandForm(forms.ModelForm):
    condition = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )
    st = (
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
       
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
    investmentproperty =forms.ChoiceField(label=False,choices=condition,required=True)
    fundsource =forms.ModelChoiceField(
        queryset=SourceOfFunding.objects.all().order_by('funding'),
        label=False,
        empty_label="Select One",
        required=True
    )
    value = forms.FloatField(label=False,required=False) 
    usefullife = forms.IntegerField(label=False,required=False)
    status = forms.ChoiceField(label=False,choices=st,required=True)
    comments = forms.CharField(
    widget=forms.Textarea(attrs={'maxlength': 255}),
        label=False,required=True)

    class Meta:
        model = Job_detail
        fields = ('accountingrecognition','amotization','usage','ipsascategory','subcategory','size','ghanapostgpsaddress','titled',
                   'methodofacquisition','investmentproperty','fundsource','value','usefullife','status','comments')
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        instance = kwargs.get("instance")
        super(JobLandForm,self).__init__(*args, **kwargs)
        
        if instance:
            self.fields['subcategory'].queryset = SubCategory.objects.filter(ipsascategory=instance.ipsascategory)
        else:
            self.fields['subcategory'].queryset = SubCategory.objects.none()
        # self.fields['product'].queryset = Products.objects.filter(tenant_id= self.request.user.devision.tenant_id,type_of_product='Capital')

        if 'ipsascategory' in self.data:
            try:
                ipsascategory = int(self.data.get('ipsascategory'))
                self.fields['subcategory'].queryset = SubCategory.objects.filter(
                    ipsascategory=ipsascategory)
            except (ValueError, TypeError):
                pass


class JobBuildingForm(forms.ModelForm):
    condition = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )
    usagetype = (
        ('Pool', 'Pool'),
        ('Assigned', 'Assigned'),
    )
    st = (
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
       
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
    status = forms.ChoiceField(label=False,choices=st,required=True)
    comments = forms.CharField(
    widget=forms.Textarea(attrs={'maxlength': 255}),
        label=False,required=True)

    class Meta:
        model = Job_detail
        fields = ('accountingrecognition','depreciation','ipsascategory','subcategory','quantity','ghanapostgpsaddress','dateplacedinservice',
        'methodofacquisition','conditions','investmentproperty','fundsource','value','usefullife','status','comments')
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        instance = kwargs.get("instance")
        super(JobBuildingForm,self).__init__(*args, **kwargs)
       
        if instance:
            
            self.fields['subcategory'].queryset = SubCategory.objects.filter(ipsascategory=instance.ipsascategory)
        else:
            
            self.fields['subcategory'].queryset = SubCategory.objects.none()
        # self.fields['product'].queryset = Products.objects.filter(tenant_id= self.request.user.devision.tenant_id,type_of_product='Capital')
        if 'ipsascategory' in self.data:
            try:
                ipsascategory = int(self.data.get('ipsascategory'))
                self.fields['subcategory'].queryset = SubCategory.objects.filter(
                    ipsascategory=ipsascategory)
            except (ValueError, TypeError):
                pass

class JobTransportForm(forms.ModelForm):
    years = [(year, str(year)) for year in range(1700, date.today().year + 1)]
    condition = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )
    usagetype = (
        ('Pool', 'Pool'),
        ('Assigned', 'Assigned'),
    )
    st = (
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
       
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
    status = forms.ChoiceField(label=False,choices=st,required=True)
    comments = forms.CharField(
    widget=forms.Textarea(attrs={'maxlength': 255}),
        label=False,required=True)

    class Meta:
        model = Job_detail
        fields = ('registrationnumber','accountingrecognition','depreciation','ipsascategory','subcategory','quantity','dateplacedinservice',
        'colour','chassisno','engineserialno','manufacturer','model','modelyear','methodofacquisition',
        'conditions','investmentproperty','fundsource','value','usefullife','status','comments')
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        instance = kwargs.get("instance")
        super(JobTransportForm,self).__init__(*args, **kwargs)
       
        if instance:
            
            self.fields['subcategory'].queryset = SubCategory.objects.filter(ipsascategory=instance.ipsascategory)
        else:
            
            self.fields['subcategory'].queryset = SubCategory.objects.none()
        # self.fields['product'].queryset = Products.objects.filter(tenant_id= self.request.user.devision.tenant_id,type_of_product='Capital')
        self.fields['manufacturer'].queryset = Brands.objects.filter(tenant_id= self.request.user.devision.tenant_id)
        if 'ipsascategory' in self.data:
            try:
                ipsascategory = int(self.data.get('ipsascategory'))
                self.fields['subcategory'].queryset = SubCategory.objects.filter(
                    ipsascategory=ipsascategory)
            except (ValueError, TypeError):
                pass

        def clean(self, *args, **kwargs):
            chassisno = self.cleaned_data['chassisno']
            engineserialno = self.cleaned_data['engineserialno']
            registrationnumber = self.cleaned_data['registrationnumber']
            chassisno_exists = FixedAsset.objects.filter(chassisno=chassisno)
            engineserialno_exists = FixedAsset.objects.filter(engineserialno=engineserialno)
            registrationnumber_exists = FixedAsset.objects.filter(registrationnumber=registrationnumber)
            
            if chassisno:
                if chassisno_exists.exists():
                    raise forms.ValidationError(
                        {'chassisno': ["An asset with this chassis number already exist"]})
            if engineserialno_exists:
                if engineserialno_exists_exists.exists():
                    raise forms.ValidationError(
                        {'engineserialno_exists': ["An asset with this engine serial number already exist"]})

            if registrationnumber:
                if registrationnumber_exists.exists():
                    raise forms.ValidationError(
                        {'registrationnumber': ["An asset with this car registration number already exist"]})
            
            return super(JobTransportForm, self).clean(*args, **kwargs)
    


class JobOutdoorForm(forms.ModelForm):
    years = [(year, str(year)) for year in range(1700, date.today().year + 1)]
    condition = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )
    usagetype = (
        ('Pool', 'Pool'),
        ('Assigned', 'Assigned'),
    )
    st = (
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
       
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
    status = forms.ChoiceField(label=False,choices=st,required=True)
    comments = forms.CharField(
    widget=forms.Textarea(attrs={'maxlength': 255}),
        label=False,required=True)

    class Meta:
        model = Job_detail
        fields = ('accountingrecognition','depreciation','ipsascategory','subcategory','quantity','ghanapostgpsaddress','dateplacedinservice',
        'chassisno','engineserialno','manufacturer','model','modelyear','methodofacquisition','conditions','investmentproperty','fundsource','value','usefullife','status','comments')
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        instance = kwargs.get("instance")
        super(JobOutdoorForm,self).__init__(*args, **kwargs)
        
        if instance:
            
            self.fields['subcategory'].queryset = SubCategory.objects.filter(ipsascategory=instance.ipsascategory)
        else:
            self.fields['subcategory'].queryset = SubCategory.objects.none()
        # self.fields['product'].queryset = Products.objects.filter(tenant_id= self.request.user.devision.tenant_id,type_of_product='Capital')
        self.fields['manufacturer'].queryset = Brands.objects.filter(tenant_id= self.request.user.devision.tenant_id)
        if 'ipsascategory' in self.data:
            try:
                ipsascategory = int(self.data.get('ipsascategory'))
                self.fields['subcategory'].queryset = SubCategory.objects.filter(
                    ipsascategory=ipsascategory)
            except (ValueError, TypeError):
                pass
    
    def clean(self, *args, **kwargs):
            chassisno = self.cleaned_data['chassisno']
            engineserialno = self.cleaned_data['engineserialno']
            
            chassisno_exists = FixedAsset.objects.filter(chassisno=chassisno)
            engineserialno_exists = FixedAsset.objects.filter(engineserialno=engineserialno)
            
            if chassisno:
                if chassisno_exists.exists():
                    raise forms.ValidationError(
                        {'chassisno': ["An asset with this chassis number already exist"]})
            if engineserialno_exists:
                if engineserialno_exists_exists.exists():
                    raise forms.ValidationError(
                        {'engineserialno_exists': ["An asset with this engine serial number already exist"]})
            
            return super(JobOutdoorForm, self).clean(*args, **kwargs)

class JobIndoorForm(forms.ModelForm):
    years = [(year, str(year)) for year in range(1700, date.today().year + 1)]
    condition = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )
    usagetype = (
        ('Pool', 'Pool'),
        ('Assigned', 'Assigned'),
    )
    st = (
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
       
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
    status = forms.ChoiceField(label=False,choices=st,required=True)
    comments = forms.CharField(
    widget=forms.Textarea(attrs={'maxlength': 255}),
        label=False,required=True)

    class Meta:
        model = Job_detail
        fields = ('accountingrecognition','depreciation','ipsascategory','subcategory','quantity','dateplacedinservice',
        'chassisno','manufacturer','methodofacquisition','conditions','investmentproperty','fundsource','value','usefullife','status','comments')
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        instance = kwargs.get("instance")
        super(JobIndoorForm,self).__init__(*args, **kwargs)
        
        if instance:
            
            self.fields['subcategory'].queryset = SubCategory.objects.filter(ipsascategory=instance.ipsascategory)
        else:
           
            self.fields['subcategory'].queryset = SubCategory.objects.none()
        self.fields['manufacturer'].queryset = Brands.objects.filter(tenant_id= self.request.user.devision.tenant_id)
        # self.fields['product'].queryset = Products.objects.filter(tenant_id= self.request.user.devision.tenant_id,type_of_product='Capital')
        if 'ipsascategory' in self.data:
            try:
                ipsascategory = int(self.data.get('ipsascategory'))
                self.fields['subcategory'].queryset = SubCategory.objects.filter(
                    ipsascategory=ipsascategory)
            except (ValueError, TypeError):
                pass
    
    def clean(self, *args, **kwargs):
        chassisno = self.cleaned_data['chassisno']
        
        chassisno_exists = FixedAsset.objects.filter(chassisno=chassisno)
        
        if chassisno:
            if chassisno_exists.exists():
                raise forms.ValidationError(
                    {'chassisno': ["An asset with this serial number already exist"]})
        
        return super(JobIndoorForm, self).clean(*args, **kwargs)


class JobWIPForm(forms.ModelForm):
    years = [(year, str(year)) for year in range(1700, date.today().year + 1)]
    accountingstatus = (
        ('In-progress','In-progress'),
        ('Completed','Completed'),
        ('Completed and Transferred','Completed and Transferred'),
       
    )
    st = (
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
       
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
    bcondition= (
        ('Good','Good'),
        ('Needs Repair/Renovation/Servicing','Needs Repair/Renovation/Servicing'),
        ('Irrepairable/Unserviceable','Irrepairable/Unserviceable'),
        ('Not Sighted','Not Sighted'),
    )
    
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
    status = forms.ChoiceField(label=False,choices=st,required=True)
    comments = forms.CharField(
    widget=forms.Textarea(attrs={'maxlength': 255}),
        label=False,required=True)

    class Meta:
        model = Job_detail
        fields = ('accountingrecognition','depreciation','ipsascategory','quantity','ghanapostgpsaddress','commencement_date',
        'expectedcompletion_date','accountingstatus','methodofacquisition','fundsource','costbf','currentperiodcost','costcf','status','comments')
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        instance = kwargs.get("instance")
        
        super(JobWIPForm,self).__init__(*args, **kwargs)

        

class RequisitionForm(forms.ModelForm):
    sts= (
        ('Capital','Capital'),
        ('Consumables','Consumables'),
         
    ) 
    requisition_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}),label=False)
    classification = forms.ChoiceField(choices = sts,label=False)
    tenant_id = forms.ModelChoiceField(label=False, queryset=Tenants.objects.all(),required=False)
    class Meta:
        model = Requisition
        fields = ('requisition_date','classification','tenant_id')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(RequisitionForm,self).__init__(*args, **kwargs)
        if self.request.user.is_superuser:
            self.fields['tenant_id'].queryset = Tenants.objects.all()
            
        else:
            self.fields['tenant_id'].queryset = Tenants.objects.filter(name=self.request.user.devision.tenant_id.name)
           
            

    def clean_driver_name(self):
        return self.cleaned_data['driver_name'].title()

class RequisitionDetailForm(forms.ModelForm):
    quantity = models.IntegerField(default=1)
    class Meta:
        model = Requisition_Details
        fields = ('quantity',)

class QuantityForm(forms.ModelForm):
    quantity_approved = forms.IntegerField(label=False)
    def clean(self, *args, **kwargs):
        quantity_approved = self.cleaned_data.get('quantity_approved')
        if quantity_approved < 1:
            
            raise forms.ValidationError(
                    {'quantity_approved': ["Quantity Approved Cannot Be Less Than 1"]})
        return super(QuantityForm, self).clean(*args, **kwargs)
    class Meta:
        model = Requisition_Details
        fields = ('quantity_approved',)


class TypeForm(forms.Form):
    sts= (
        ('Staff','Staff'),
        ('Pool','Pool'),
    ) 
    type_of_issue = forms.ChoiceField(choices = sts,label=False)


class AllocationForm(forms.ModelForm):
    
    allocation_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}),label=False)
    description = forms.CharField(label=False)
    
    class Meta:
        model = Allocation
        fields = ('allocation_date','description')

    def clean_describtion(self):
        return self.cleaned_data['description'].title()

class AllocationDestinantionForm(forms.ModelForm):
    sts= (
        ('Capital','Capital'),
        ('Consumables','Consumables'),
         
    ) 
    devision = forms.ModelChoiceField(label=False, queryset=Devision.objects.filter(status = True))
    classification = forms.ChoiceField(choices = sts,label=False)
    class Meta:
        model = Allocation_Destination
        fields = ('devision','classification')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(AllocationDestinantionForm,self).__init__(*args, **kwargs)
        self.fields['devision'].queryset = Devision.objects.filter(tenant_id=self.request.user.devision.tenant_id.id,status = True)

class EditAllocationDestinantionForm(forms.ModelForm):
    devision = forms.ModelChoiceField(label=False, queryset=Devision.objects.filter(status = True))
    sub_division = forms.ModelChoiceField(queryset=Sub_Devision.objects.all(),label=False)
    class Meta:
        model = Allocation_Destination
        fields = ('devision','sub_division')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(AllocationDestinantionForm,self).__init__(*args, **kwargs)
       
        self.fields['devision'].queryset = Devision.objects.filter(tenant_id=self.request.user.devision.tenant_id.id,status = True)
        if 'devision' in self.data:
            try:
                devision = int(self.data.get('devision'))
                self.fields['sub_division'].queryset = Sub_Devision.objects.filter(
                    devision=devision)
            except (ValueError, TypeError):
                pass