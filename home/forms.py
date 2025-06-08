from django.forms import ModelForm
from .models import Student
from django import forms
from .models import UploadFileForm


class StudForm(ModelForm):
    class Meta:
        model=Student
        fields=[ "rollnumber", "name", "age", "email", "address",
            "physics", "chemistry", "maths", "english",
            "totalmarks", "maxmarks", "percentage"]


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadFileForm
        fields = ['file']        


