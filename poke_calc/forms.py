from django import forms
from .models import Pokemon
import logging

logger = logging.getLogger('baseLogger')

class PokeForm(forms.Form):
    '''
    This form is used to let users select pokemon they wish to view information about.
    '''
    pass

class EvolutionForm(forms.Form):
    '''
    This form is used to let users identify which pokemon they want to evaluate the evolution of.
    '''
    pokemon = forms.ChoiceField(choices=[(x.get_poke_id(), x.get_name()) for x in Pokemon.objects.all()])
    indiv_atk = forms.IntegerField(min_value=0, max_value=15)
    indiv_def = forms.IntegerField(min_value=0, max_value=15)
    indiv_sta = forms.IntegerField(min_value=0, max_value=15)
    cp = forms.IntegerField(min_value=10)
