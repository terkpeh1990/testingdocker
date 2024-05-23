from django import forms
from .models import *
from django.forms.widgets import NumberInput
from company.models import Devision,Sub_Devision
from datetime import date
from authentication.models import User

class TeamForm(forms.ModelForm):
    """Form definition for MODELNAME."""
    name = forms.CharField(label=False)

    class Meta:
        """Meta definition for MODELNAMEform."""

        model = Teams
        fields = ('name',)

class LevelForm(forms.ModelForm):
    """Form definition for Level."""
    name = forms.CharField(label=False)
    class Meta:
        """Meta definition for Levelform."""

        model = Level
        fields = ('name',)

class AgentForm(forms.ModelForm):
    """Form definition for Agent."""
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
    agent = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label=False,
        empty_label="Select One",
        required=True
    )
    team = forms.ModelChoiceField(
        queryset=Teams.objects.all(),
        label=False,
        empty_label="Select One",
        required=True
    )
    level = forms.ModelChoiceField(
        queryset=Level.objects.all(),
        label=False,
        empty_label="Select One",
        required=True
    )

    class Meta:
        """Meta definition for Agentform."""

        model = Agent
        fields = ('costcenter','subcostcenter','agent','team','level')
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        instance = kwargs.get("instance")
        super(AgentForm,self).__init__(*args, **kwargs)
        if self.request.user.is_superuser:
            self.fields['costcenter'].queryset = Devision.objects.filter(status = True)
            
        else:
            self.fields['costcenter'].queryset = Devision.objects.filter(tenant_id=self.request.user.devision.tenant_id.id,status = True)
           
        if instance:
            self.fields['subcostcenter'].queryset = Sub_Devision.objects.filter(devision=instance.costcenter)
            self.fields['agent'].queryset = User.objects.filter(sub_division=instance.subcostcenter)
        else:
            self.fields['subcostcenter'].queryset = Sub_Devision.objects.none()
            self.fields['agent'].queryset = User.objects.none()


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
                self.fields['agent'].queryset = User.objects.filter(
                    sub_division=subcostcenter)
            except (ValueError, TypeError):
                pass


class TicketForm(forms.ModelForm):
    """Form definition for Ticket."""
    subject = forms.CharField(label=False,)
    description = forms.CharField(label=False, widget=forms.Textarea)
    costcenter = forms.ModelChoiceField(
        queryset=Devision.objects.all().order_by('name'),
        label=False,
        empty_label="Select One",
        required=False
    )
    subcostcenter =forms.ModelChoiceField(
        queryset=Sub_Devision.objects.all(),
        label=False,
        empty_label="Select One",
        required=False
    )
    ticketuser = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label=False,
        empty_label="Select One",
        required=False
    )

    class Meta:
        """Meta definition for Ticketform."""

        model = Ticket
        fields = ('subject','description','costcenter','subcostcenter','ticketuser')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        instance = kwargs.get("instance")
        super(TicketForm,self).__init__(*args, **kwargs)
        if self.request.user.is_superuser:
            self.fields['costcenter'].queryset = Devision.objects.filter(status = True)
            
        else:
            self.fields['costcenter'].queryset = Devision.objects.filter(tenant_id=self.request.user.devision.tenant_id.id,status = True)
           
        if instance:
            self.fields['subcostcenter'].queryset = Sub_Devision.objects.filter(devision=instance.costcenter)
            self.fields['ticketuser'].queryset = User.objects.filter(sub_division=instance.subcostcenter)
        else:
            self.fields['subcostcenter'].queryset = Sub_Devision.objects.none()
            self.fields['ticketuser'].queryset = User.objects.none()


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
                self.fields['ticketuser'].queryset = User.objects.filter(
                    sub_division=subcostcenter)
            except (ValueError, TypeError):
                pass

class AssignedTicketForm(forms.ModelForm):
    """Form definition for AssignedTicket."""
    priority = (
            ('Low', 'Low'),
            ('Medium', 'Medium'),
            ('High', 'High'),
        )
    level =forms.ModelChoiceField(
        queryset=Level.objects.all(),
        label=False,
        empty_label="Select One",
        required=True
    )
    agent =forms.ModelChoiceField(
        queryset=Agent.objects.all(),
        label=False,
        empty_label="Select One",
        required=True
    )
    priority =forms.ChoiceField(label=False,choices=priority,required=True)
    
    
    class Meta:
        """Meta definition for AssignedTicketform."""

        model = AgentTicket
        fields = ('level','agent','priority')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(AssignedTicketForm,self).__init__(*args, **kwargs)
        
        self.fields['level'].queryset = Level.objects.all()
        self.fields['agent'].queryset = Agent.objects.none()

        if 'level' in self.data:
            try:
                level = int(self.data.get('level'))
                self.fields['agent'].queryset = Agent.objects.filter(
                    level=level)
            except (ValueError, TypeError):
                pass

class CommentForm(forms.ModelForm):
    """Form definition for Comment."""
    comment = forms.CharField(
                widget=forms.Textarea(attrs={'maxlength': 1200}),
                    label=False,
                    required=True)
    class Meta:
        """Meta definition for Commentform."""

        model = AgentComment
        fields = ('comment',)

class CloseTicketForm(forms.ModelForm):
    """Form definition for CloseTiccket."""
    status = (
            ('Closed', 'Closed'),
        )
    status = forms.ChoiceField(label=False,choices=status,required=True)
    class Meta:
        """Meta definition for CloseTiccketform."""

        model = AgentTicket
        fields = ('status',)
