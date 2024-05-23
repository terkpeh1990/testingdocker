from django import forms
from django.contrib.auth import authenticate, get_user_model,password_validation
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django.contrib.auth.models import Group, Permission
from .import models
from .models import *
from company.models import *




User = get_user_model()

class UserLoginForm(forms.Form):
    email = forms.CharField(label=False, widget=forms.TextInput(
        attrs={'placeholder': 'Please Enter Email'}))
    password = forms.CharField(label=False, widget=forms.PasswordInput(
        attrs={'placeholder': 'Please Enter Password'}))

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError('Username or Password incorrect')
            if not user.check_password(password):
                raise forms.ValidationError('Username or Password incorrect')
            if not user.is_active:
                raise forms.ValidationError('Username or Password incorrect')
        return super(UserLoginForm, self).clean(*args, **kwargs)

    class Meta():
        model = User
        fields = ('email', 'password')


class UserGroupForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.filter(codename__icontains='custom'),
        widget=forms.CheckboxSelectMultiple,
        label=False
    )
    name = forms.CharField(label=False)
    class Meta:
        model = Group
        fields = ('name','permissions')

    def clean(self, *args, **kwargs):
        name = self.cleaned_data.get('name')
        name_exists = Group.objects.filter(name=name.title()) 
        if name:
            if name_exists.exists():
                raise forms.ValidationError(
                    {'name': ["A Group with this name already exist"]})
        return super(UserGroupForm, self).clean(*args, **kwargs)

class UserGroupEditForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.filter(codename__icontains='custom'),
        widget=forms.CheckboxSelectMultiple,
        label=False
    )
    name = forms.CharField(label=False)
    class Meta:
        model = Group
        fields = ('name','permissions')

class GradeForm(forms.ModelForm):
    name = forms.CharField(label=False)
    class Meta:
        model = Grade
        fields = ('name',)


class UploadFileForm(forms.Form):
    file = forms.FileField(label=False)

class CreateUserForm(UserCreationForm):
    stat =(
        ('Yes','Yes'),
        ('No','No'),
    )
    staffid = forms.CharField(label=False)
    last_name = forms.CharField(label=False)
    first_name = forms.CharField(label=False)
    phone_number = forms.CharField(label=False)
    devision = forms.ModelChoiceField(label=False, queryset=Devision.objects.filter(status = True))
    sub_division = forms.ModelChoiceField(queryset=Sub_Devision.objects.all(),label=False)
    grade = forms.ModelChoiceField(queryset=Grade.objects.all(),label=False)
    group = forms.ModelChoiceField(queryset=Group.objects.all(),label=False)
    user_permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.filter(codename__icontains='custom'),
        widget=forms.CheckboxSelectMultiple,
        label=False,
        required = False,
    )
    email = forms.CharField(label=False)
    password1 = forms.CharField(label=False, widget=forms.PasswordInput)
    password2 = forms.CharField(label=False, widget=forms.PasswordInput)
   

    class Meta:
        model = User
        fields = ('staffid','last_name','first_name','phone_number','devision', 'sub_division', 'grade','group','email','password1', 'password2','user_permissions')
    
    def clean_first_name(self):
        return self.cleaned_data['first_name'].title()

    def clean_last_name(self):
        return self.cleaned_data['last_name'].title()

    def clean_staffid(self):
        return self.cleaned_data['staffid'].title()

    def clean_email(self):
        return self.cleaned_data['email'].lower()

    def clean_phone_number(self):
        return self.cleaned_data['phone_number'].title()
    
    def clean_email_staff(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        staffid = self.cleaned_data.get('staffid')
        email_exists = User.objects.filter(email=email)
        staffid_exist = User.objects.filter(staffid=staffid)
        if email:
            if email_exists.exists():
                raise forms.ValidationError(
                    {'email': ["A user with this email address already exist"]})
        if staffid:
            if staffid_exist.exists():
                raise forms.ValidationError(
                    {'staffid': ["A user with this staff id address already exist"]})

        return super(CreateUserForm, self).clean(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(CreateUserForm,self).__init__(*args, **kwargs)
        if self.request.user.is_superuser:
            self.fields['devision'].queryset = Devision.objects.filter(status = True)
            self.fields['grade'].queryset = Grade.objects.all()
        else:
            self.fields['devision'].queryset = Devision.objects.filter(tenant_id=self.request.user.devision.tenant_id.id,status = True)
            self.fields['grade'].queryset = Grade.objects.filter(tenant_id=self.request.user.devision.tenant_id.id)
        self.fields['sub_division'].queryset = Sub_Devision.objects.none()

        if 'devision' in self.data:
            try:
                devision = int(self.data.get('devision'))
                self.fields['sub_division'].queryset = Sub_Devision.objects.filter(
                    devision=devision)
            except (ValueError, TypeError):
                pass

class UpdateUserForm(forms.ModelForm):
    staffid = forms.CharField(label=False)
    last_name = forms.CharField(label=False)
    first_name = forms.CharField(label=False)
    phone_number = forms.CharField(label=False)
    devision = forms.ModelChoiceField(label=False, queryset=Devision.objects.all())
    sub_division = forms.ModelChoiceField(label=False, queryset=Sub_Devision.objects.all())
    grade = forms.ModelChoiceField(queryset=Grade.objects.all(),label=False)
    group = forms.ModelChoiceField(queryset=Group.objects.all(),label=False)
    email = forms.CharField(label=False)
    user_permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.filter(codename__icontains='custom'),
        widget=forms.CheckboxSelectMultiple,
        label=False,
        required = False,
    )
   

    class Meta:
        model = User
        fields = ('staffid','last_name','first_name','phone_number','devision', 'sub_division','grade', 'group','email','user_permissions')
    
    def clean_first_name(self):
        return self.cleaned_data['first_name'].title()

    def clean_last_name(self):
        return self.cleaned_data['last_name'].title()

    def clean_staffid(self):
        return self.cleaned_data['staffid'].title()

    def clean_email(self):
        return self.cleaned_data['email'].lower()

    def clean_phone_number(self):
        return self.cleaned_data['phone_number'].title()
    
    def clean_email_staff(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        staffid = self.cleaned_data.get('staffid')
        email_exists = User.objects.filter(email=email)
        staffid_exist = User.objects.filter(staffid=staffid)
        if email:
            if email_exists.exists():
                raise forms.ValidationError(
                    {'email': ["A user with this email address already exist"]})
        if staffid:
            if staffid_exist.exists():
                raise forms.ValidationError(
                    {'staffid': ["A user with this staff id address already exist"]})

        return super(UpdateUserForm, self).clean(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(UpdateUserForm,self).__init__(*args, **kwargs)
        if self.request.user.is_superuser:
            self.fields['devision'].queryset = Devision.objects.filter(status = True)
            self.fields['grade'].queryset = Grade.objects.all()
        else:
            self.fields['devision'].queryset = Devision.objects.filter(tenant_id=self.request.user.devision.tenant_id.id,status = True)
            self.fields['grade'].queryset = Grade.objects.filter(tenant_id=self.request.user.devision.tenant_id.id)

        if 'devision' in self.data:
            try:
                devision = int(self.data.get('devision'))
                self.fields['sub_division'].queryset = Sub_Devision.objects.filter(
                    devision=devision)
            except (ValueError, TypeError):
                pass


                

class UserUpdateUserForm(forms.ModelForm):
    staffid = forms.CharField(label=False)
    last_name = forms.CharField(label=False)
    first_name = forms.CharField(label=False)
    phone_number = forms.CharField(label=False)
    email = forms.CharField(label=False)
    devision = forms.ModelChoiceField(label=False, queryset=Devision.objects.all())
    sub_division = forms.ModelChoiceField(label=False, queryset=Sub_Devision.objects.all())
    grade = forms.ModelChoiceField(queryset=Grade.objects.all(),label=False)
    
   

    class Meta:
        model = User
        fields = ('staffid','last_name','first_name','phone_number','email','devision','sub_division','grade')
    
    def clean_first_name(self):
        return self.cleaned_data['first_name'].title()

    def clean_last_name(self):
        return self.cleaned_data['last_name'].title()

    def clean_staffid(self):
        return self.cleaned_data['staffid'].title()

    def clean_email(self):
        return self.cleaned_data['email'].lower()

    def clean_phone_number(self):
        return self.cleaned_data['phone_number'].title()
    
    def clean_email_staff(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        staffid = self.cleaned_data.get('staffid')
        email_exists = User.objects.filter(email=email)
        staffid_exist = User.objects.filter(staffid=staffid)
        if email:
            if email_exists.exists():
                raise forms.ValidationError(
                    {'email': ["A user with this email address already exist"]})
        if staffid:
            if staffid_exist.exists():
                raise forms.ValidationError(
                    {'staffid': ["A user with this staff id address already exist"]})

        return super(UserUpdateUserForm, self).clean(*args, **kwargs)
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(UpdateUserForm,self).__init__(*args, **kwargs)
        if self.request.user.is_superuser:
            self.fields['devision'].queryset = Devision.objects.filter(status = True)
            self.fields['grade'].queryset = Grade.objects.all()
        else:
            self.fields['devision'].queryset = Devision.objects.filter(tenant_id=self.request.user.devision.tenant_id.id,status = True)
            self.fields['grade'].queryset = Grade.objects.filter(tenant_id=self.request.user.tenant_id.id)

        if 'devision' in self.data:
            try:
                devision = int(self.data.get('devision'))
                self.fields['sub_division'].queryset = Sub_Devision.objects.filter(
                    devision=devision)
            except (ValueError, TypeError):
                pass

    

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password','placeholder': 'Old Password'})
    )
    new_password1 = forms.CharField(
        label=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','placeholder': 'New Password'}),
        validators=[password_validation.validate_password]
    )
    new_password2 = forms.CharField(
        label=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','placeholder': 'Confirm Password'})
    )
   