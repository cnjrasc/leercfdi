from django import forms
from .models import Contribuyente
#from .models import Cfdi



class ContribuyenteForm(forms.ModelForm):
    class Meta:
        model = Contribuyente
        fields ='__all__'

#class CfdiForm(forms.ModelForm):
    #class Meta:
        #model = Cfdi
        #fields ='__all__'

class CFDIUploadForm(forms.Form):
    xml_file = forms.FileField(label="Subir archivo CFDI (XML)")

class CFDIZipForm(forms.Form):
    zip_file = forms.FileField(label="Subir ZIP con CFDIs XML")

