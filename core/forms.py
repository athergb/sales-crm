from django import forms
from .models import Visit, Client

class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        exclude = ['agent', 'visit_date'] 
        widgets = {
            'summary': forms.Textarea(attrs={'rows': 4}),
        }

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'phone', 'address', 'visiting_card', 'client_type']        