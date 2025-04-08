from django import forms
from .models import*

class EksportSargytForm(forms.ModelForm):
    class Meta:
        model = EksportSargyt
        fields = '__all__'
        
class ImportHasabatForm(forms.ModelForm):
    class Meta:
        model = ImportHasabat
        fields = '__all__'        
