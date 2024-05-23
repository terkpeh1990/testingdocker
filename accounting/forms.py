from django import forms
from .models import *
from authentication.models import User
from django.forms.widgets import NumberInput

class CurrencyForm(forms.ModelForm):
    name = forms.CharField(label=False)
    symbol = forms.CharField(label=False)
    rate = forms.DecimalField(label=False)
   
    class Meta:
        model = Currency
        fields = ('name','symbol','rate')

    
    
class AccountClassForm(forms.ModelForm):
    code = forms.CharField(label=False)
    name = forms.CharField(label=False)
    
    class Meta:
        model = Account_Class
        fields = ('code','name')

    def clean(self, *args, **kwargs):
        code = self.cleaned_data['code']
        code_exists = Account_Class.objects.filter(code=code)
        if code:
            if self.instance._state.adding and code_exists.exists():
                raise forms.ValidationError(
                    {'code': ["This Code Already Exist"]})
        return super(AccountClassForm, self).clean(*args, **kwargs)

class AccountItemForm(forms.ModelForm):
    code = forms.CharField(label=False)
    name = forms.CharField(label=False)
    
    class Meta:
        model = AccountItem
        fields = ('code','name')

    def clean(self, *args, **kwargs):
        code = self.cleaned_data['code']
        code_exists = AccountItem.objects.filter(code=code)
        if code:
            if self.instance._state.adding  and 0 < int(code)  > 10:
                raise forms.ValidationError(
                    {'code': ["This Code only be start from 1 and end at 9 "]})
        return super(AccountItemForm, self).clean(*args, **kwargs)

class AccountSubItemForm(forms.ModelForm):
    code = forms.CharField(label=False)
    name = forms.CharField(label=False)
    
    class Meta:
        model = AccountSubItem
        fields = ('code','name')

class AccountSubSubItemForm(forms.ModelForm):
    account_number = forms.CharField(label=False)
    name = forms.CharField(label=False)
    
    class Meta:
        model = AccountLedger
        fields = ('account_number','name')


class FiscalYearForm(forms.ModelForm):
    start = forms.DateField(widget=NumberInput(attrs={'type': 'date'}),label=False,required=True)
    end = forms.DateField(widget=NumberInput(attrs={'type': 'date'}),label=False,required=True)
    
    class Meta:
        model = Fiscal_year
        fields = ('start','end')

class BanktypeForm(forms.ModelForm):
    name = forms.CharField(label=False)
   
    class Meta:
        model = BankAccountsType
        fields = ('name',)

class PvForm(forms.ModelForm):
    type_of_pay= (
        ('Third Party','Third Party'),
        ('Refund','Refund'),
        ('Accountable Imprest','Accountable Imprest'),
    )
    pvmode= (
        ('GIFMIS','GIFMIS'),
        ('Internal','Internal'),
        
    )
    pvtype= (
        ('General','General'),
        ('Honorarium','Honorarium'),
    )
    status= (
        ('Pending','Pending'),
        ('Cancelled','Cancelled'),
        ('Approved','Approved'),
        ('Authorised','Authorised'),
        ('Authorised & Passed','Authorised & Passed'),
        ('Check No Entered','Check No Entered'),
        ('Pv Eligibility','Pv Eligibility'),
        ('Paid','Paid'), 
    )
    tax= (
        ('Yes','Yes'),
        ('No','No'),
        
    )
    pv_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}),label=False,required=True)
    type_of_pay =forms.ChoiceField(choices = type_of_pay,label=False)
    mode_of_pv= forms.ChoiceField(choices = pvmode,label=False)
    type_of_pv= forms.ChoiceField(choices = pvtype,label=False)
    withholding_tax =forms.ChoiceField(choices = tax,label=False)
    withholding_tax_amount=forms.FloatField(label=False,required=False,initial=0.0) 
    bankaccounttype = forms.ModelChoiceField(label=False, queryset=SubDevisionAccountType.objects.all())
    currency_id = forms.ModelChoiceField(label=False, queryset=Currency.objects.all())
    warrant_no=forms.CharField(label=False)

    class Meta:
        model = PaymentVoucher
        fields = ('pv_date','type_of_pay','mode_of_pv','type_of_pv','withholding_tax','withholding_tax_amount','bankaccounttype','currency_id','warrant_no',)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(PvForm,self).__init__(*args, **kwargs)
        self.fields['bankaccounttype'].queryset = SubDevisionAccountType.objects.filter(sub_division=self.request.user.sub_division)

    def clean(self, *args, **kwargs):
        withholding_tax = self.cleaned_data.get('withholding_tax')
        withholding_tax_amount = self.cleaned_data.get('withholding_tax_amount')
        if withholding_tax_amount:
            tax = withholding_tax_amount
        else:
            tax = 0.00
        if withholding_tax == "Yes" and tax <= 0.00 :
            raise forms.ValidationError(
                    {'withholding_tax_amount': ["Withholding Tax Percentage Cannot Be Less or Equal to 0 % "]})
        return super(PvForm, self).clean(*args, **kwargs)


class NoDocPvForm(forms.ModelForm):
    type_of_pay= (
        ('Third Party','Third Party'),
        ('Refund','Refund'),
        ('Accountable Imprest','Accountable Imprest'),
    )
    pvmode= (
        ('GIFMIS','GIFMIS'),
        ('Internal','Internal'),
        
    )
    pvtype= (
        ('General','General'),
        ('Honorarium','Honorarium'),
    )
    status= (
        ('Pending','Pending'),
        ('Cancelled','Cancelled'),
        ('Approved','Approved'),
        ('Authorised','Authorised'),
        ('Authorised & Passed','Authorised & Passed'),
        ('Check No Entered','Check No Entered'),
        ('Pv Eligibility','Pv Eligibility'),
        ('Paid','Paid'), 
    )
    tax= (
        ('Yes','Yes'),
        ('No','No'),
        
    )
    pv_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}),label=False,required=True)
    type_of_pay =forms.ChoiceField(choices = type_of_pay,label=False)
    mode_of_pv= forms.ChoiceField(choices = pvmode,label=False)
    type_of_pv= forms.ChoiceField(choices = pvtype,label=False)
    withholding_tax =forms.ChoiceField(choices = tax,label=False)
    withholding_tax_amount=forms.FloatField(label=False,required=False,initial=0.0) 
    payto = forms.CharField(label=False)
    pay_to_address = forms.CharField(label=False)
    description = forms.CharField(label=False)
    bankaccounttype = forms.ModelChoiceField(label=False, queryset=SubDevisionAccountType.objects.all())
    currency_id = forms.ModelChoiceField(label=False, queryset=Currency.objects.all())
    warrant_no=forms.CharField(label=False)

    class Meta:
        model = PaymentVoucher
        fields = ('pv_date','type_of_pay','mode_of_pv','type_of_pv','withholding_tax','withholding_tax_amount','payto','pay_to_address','description','bankaccounttype','currency_id','warrant_no',)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(NoDocPvForm,self).__init__(*args, **kwargs)
        self.fields['bankaccounttype'].queryset = SubDevisionAccountType.objects.filter(sub_division=self.request.user.sub_division)

    def clean(self, *args, **kwargs):
        withholding_tax = self.cleaned_data.get('withholding_tax')
        withholding_tax_amount = self.cleaned_data.get('withholding_tax_amount')
        if withholding_tax_amount:
            tax = withholding_tax_amount
        else:
            tax = 0.00
        if withholding_tax == "Yes" and tax <= 0.00 :
            raise forms.ValidationError(
                    {'withholding_tax_amount': ["Withholding Tax Percentage Cannot Be Less or Equal to 0 % "]})
        return super(NoDocPvForm, self).clean(*args, **kwargs)
    
class PvDetailForm(forms.ModelForm):
    amount = forms.FloatField(label=False) 
    description=forms.CharField(label=False)

    class Meta:
        model = PvDetail
        fields = ('amount','description')

    def clean(self, *args, **kwargs):
        amount = self.cleaned_data['amount']
        if amount < 1:
            raise forms.ValidationError(
                    {'amount': ["Amount Cannot be less than GHC 1.00 "]})
        return super(PvDetailForm, self).clean(*args, **kwargs)



class ChequeForm(forms.ModelForm):
    status= (
        ('Posted','Posted'),
        ('Pending','Pending'),
        
    )
    type_of_payment= (
        ('Self','Self'),
        ('Others','Others'),
        
    )
    cheque_number_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}),label=False,required=True)
    type_of_payment=forms.ChoiceField(choices = type_of_payment,label=False,required=True)
    pv_number = forms.CharField(required=False,label=False)
    cheque_number = forms.CharField(label=False,required=True)
    amount = forms.FloatField(label=False,required=True) 

    class Meta:
        model = PvPayment
        fields = ('cheque_number_date','type_of_payment','cheque_number','amount')
    
    def clean(self, *args, **kwargs):
        amount = self.cleaned_data['amount']
        type_of_payment = self.cleaned_data['type_of_payment']
        pv_number = self.cleaned_data['pv_number']
        checking=['Check No Entered','Paid','Payee Notified']
        
        if amount < 1:
            raise forms.ValidationError(
                    {'amount': ["Amount Cannot be less than GHC 1.00 "]})
        if pv_number:
            pv_number_exists = PaymentVoucher.objects.filter(id=pv_number,status__in=checking)
            if not pv_number_exists:
                raise forms.ValidationError(
                        {'pv_number': ["Payment Voucher with this number does not exist or can't be used to make payment"]})
        
        if type_of_payment and pv_number and amount:
            pv_number_exists = PaymentVoucher.objects.filter(id=pv_number)
            if pv_number_exists and pv_number_exists.pv_amount < amount:
                raise forms.ValidationError(
                        {'pv_number': ["The payment voucher balance is not enough to pay for this pv"]})

        return super(ChequeForm, self).clean(*args, **kwargs)
    


class ComfirmForm(forms.ModelForm):
    # amount = forms.FloatField(attrs={'type': 'readonly'},label=False)
    amount = forms.FloatField(label=False) 
    comfirm = forms.CharField(label=False) 
    code = forms.CharField(widget=forms.HiddenInput()) 
    
    class Meta:
        model = PaymentVoucherBeneficiary
        fields = ('code','comfirm')

    # def __init__(self, *args, **kwargs):
    #     super(ComfirmForm, self).__init__(*args, **kwargs)
    #     instance = getattr(self, 'instance', None)
    #     if instance and instance.id:
            
    #         self.fields['amount'].widget.attrs['disabled'] = 'disabled'

    def clean(self, *args, **kwargs):
        # amount = self.cleaned_data.get('amount')
        comfirm =self.cleaned_data.get('comfirm')
        code =self.cleaned_data.get('code')
        if comfirm != code:
            raise forms.ValidationError(
                    {'comfirm': ["Invalid Funds Release Code"]})
        return super(ComfirmForm, self).clean(*args, **kwargs)

class InternalAuditForm(forms.ModelForm):
    stat =(
        ('Completed','Completed'),
        ('Returned','Returned'),
        ('Cancelled','Cancelled')
    )
    source =(
            ('GOG','GOG'),
            ('Others', 'Others')
          )
    pv =(
        ('General','General'),
        ('Honorarium','Honorarium')
       )
    center=(
        ('Cost Center 1','Cost Center 1'),
        ('Cost Center 2','Cost Center 2'),
        ('Cost Center 3','Cost Center 3'),
        ('Cost Center 4','Cost Center 4'),
        ('Cost Center 5','Cost Center 5')
           )
    stat =(
        ('Completed','Completed'),
        ('Returned','Returned'),
        ('Cancelled','Cancelled')
    )
    ia_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}),label=False,required=True)
    source_of_funding =forms.ChoiceField(choices = source,label=False)
    cost_center =forms.ChoiceField(choices = center,label=False)
    description = forms.CharField(label=False)
    status = forms.ChoiceField(choices = stat,label=False)
    remarks=forms.CharField(
        widget=forms.Textarea(attrs={'maxlength': 1200}),
        label=False,required=False)
    # return_to_chest = forms.FloatField(label=False,required=False,initial=0.0)
    # return_to_chest_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}),label=False)


    class Meta:
        model = Pveligibility
        fields = ('ia_date','source_of_funding','cost_center','description','status','remarks',)

    def clean(self, *args, **kwargs):
        status = self.cleaned_data.get('status')
        remarks = self.cleaned_data.get('remarks')
        # return_to_chest = self.cleaned_data.get('return_to_chest')
        # return_to_chest_date = self.cleaned_data.get('return_to_chest_date')
        if status:
            if status == 'Cancelled' or status == 'Returned' and not remarks :
                raise forms.ValidationError(
                        {'remarks': ["Please provide a reason for Returning or cancelling Pv "]})
        # if return_to_chest:
        #     if return_to_chest > 0.00 and not return_to_chest_date:
        #         raise forms.ValidationError(
        #                 {'remarks': ["Please Select a Return Date "]},
        #                 {{'return_to_chest_date': ["Please provide a reason for the amount returned to chest"]}})

        return super(InternalAuditForm, self).clean(*args, **kwargs)


class ImpressForm(forms.ModelForm):
    impress_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}),label=False,required=True)
    claim_detail = forms.CharField(widget=forms.Textarea(attrs={'maxlength': 1200}),
        label=False,)
    amount = forms.FloatField(label=False) 
    
    class Meta:
        model = Imprest
        fields = ('impress_date','claim_detail','amount')

class ImpressactualExpenseForm(forms.Form):
    actual_expense = forms.FloatField(label=False) 
    def clean(self, *args, **kwargs):
        actual_expense = self.cleaned_data.get('actual_expense')
        if actual_expense:
            if actual_expense < 0 :
                raise forms.ValidationError(
                        {'actual_expense': ["Amount Cannot < 0 "]})
        return super(ImpressactualExpenseForm, self).clean(*args, **kwargs)
    
    