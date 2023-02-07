
from django import forms 
from .models import Database
class addModelForm(forms.ModelForm):
    class Meta:
        model=Database
        fields=['Cardnum','Date','Merchnum','Merch_description','Merch_state','Merch_zip','Transtype','Amount']
