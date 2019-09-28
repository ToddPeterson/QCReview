from django import forms

from . import config
from .models import QCRun

def get_codelines():
    return [(x[0], x[0]) for x in QCRun.objects.values_list('codeline').distinct()]

def get_changelists():
    return [(x[0], x[0]) for x in QCRun.objects.values_list('cl').distinct()]

class QCRunSelectForm(forms.Form):
    codeline = forms.ChoiceField(choices=get_codelines)
    changelist = forms.ChoiceField(choices=get_changelists)
