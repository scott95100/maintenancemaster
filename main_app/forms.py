from django import forms
from .models import Maintenance, Machine

class MaintenanceForm(forms.ModelForm):
    # meta class beacuse that's how django can do it
    class Meta:
        # which model
        model = Maintenance
        fields = ['date', 'job']

# added a catform
class MachineForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = ('name', 'operator', 'manufacturedYear', 'partNumber')