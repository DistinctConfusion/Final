from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from document.models import Project, Specification

class ProjectForm(forms.ModelForm):
    class Meta: 
        model = Project
        fields = ('proj_name',)


class SpecificationForm(forms.ModelForm):
    class Meta:
        model = Specification
        fields = ('spec_name', 'description',)
