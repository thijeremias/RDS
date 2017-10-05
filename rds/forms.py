from django import forms

class UploadFileForm(forms.Form):
    arquivo  = forms.FileField()