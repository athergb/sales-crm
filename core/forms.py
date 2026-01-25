from django import forms
from .models import Visit, Client, Agency

# 1. Updated Visit Form
class VisitForm(forms.ModelForm):
    # visit_date will be a Calendar widget in HTML
    visit_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False # If blank, defaults to today
    )
    
    class Meta:
        model = Visit
        # Fields required based on your request
        fields = ['agency', 'contact_person', 'mobile_number', 'email_address', 'type_of_business', 'remarks', 'visit_date']
        widgets = {
            'remarks': forms.Textarea(attrs={'rows': 4}),
        }

# 2. Agency Form (For Admin to add agencies)
class AgencyForm(forms.ModelForm):
    class Meta:
        model = Agency
        fields = '__all__'

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'phone', 'address', 'visiting_card', 'client_type']