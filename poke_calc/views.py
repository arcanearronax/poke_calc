from django.http import HttpResponse
from django.views import View
from django.template import loader
from .models import Pokemon, PokemonStats, Evolution
from .forms import EvolutionForm
import logging

logger = logging.getLogger('baselogger')

class HomeView(View):

    def get(self, request, *args, **kwargs):
        logger.info('PokeView.get: Enter')

        template = loader.get_template('base.html')
        context = {
            'message': 'IT WORKS',
        }
        return HttpResponse(template.render(context, request))

class PokemonView(View):
    '''
    This is used to serve requests for pokemon.
    '''

    def get(self, request, *args, **kwargs):
        '''
        This is used to return information for a given pokemon.
        '''
        logger.info('PokemonView.get: {} - {}'.format(args, kwargs))
        template = loader.get_template('pokemon.html')
        pokemon_name = kwargs['pokemon_name']
        logger.info('found: {}'.format(pokemon_name))
        pokemon = Pokemon.get_by_name(pokemon_name)
        context = {
            'pokemon_name': pokemon.get_name(),
            'base_atk': pokemon.get_base_atk(),
            'base_def': pokemon.get_base_def(),
            'base_sta': pokemon.get_base_sta(),
        }

        return HttpResponse(template.render(context, request))

class EvolutionView(View):
    '''
    This is used to serve requests for the evolution calculator.
    '''

    def get(self, request):
        '''
        This is used to serve pages for the user to select pokemon.
        '''
        logger.info('EvolutionView.get: Enter')

        template = loader.get_template('calculator.html')
        context = {
            'page_title': 'Evolution Calculator',
            'page_description': "This is used to identify a pokemon's final evolution's stats",
            'form': EvolutionForm,
        }

        return HttpResponse(template.render(context, request))

    def post(self, request):
        '''
        This is used to respond to requests for pokemon evolutions
        '''
        logger.info('EvolutionView.post: Enter')

        # Validate the form
        form = EvolutionForm(request.POST)

        if form.is_valid():
            logger.info('EvolutionView.post: form is valid')

            # Get the submitted info
            poke_name = form.cleaned_data['pokemon']
            indiv_atk = form.cleaned_data['indiv_atk']
            indiv_def = form.cleaned_data['indiv_def']
            indiv_sta = form.cleaned_data['indiv_sta']
            cp = form.cleaned_data['cp']

            # Get the pokemon's poke_id
            logger.info('The form says: {} {} {} {}'.format(poke_name, indiv_atk, indiv_def, indiv_sta))
            poke_id = Pokemon.get_by_name(poke_name)
            logger.info('Pokemon: {}'.format(poke_id))

            # Get provided pokemon's level
            level = PokemonStats.validate_stats(poke_id, indiv_atk, indiv_def, indiv_sta, cp), 'Invalid Stats Provided'

            # Identify the possible evolutions
            poke_list = Evolution.get_evolutions(poke_id)

            # Calculate the evolution data here

            template = loader.get_template('calculator.html')
            context = {
                'page_title': 'Evolution Calculator',
                'page_description': "Here are the pokemon's results",
                'form': EvolutionForm,
                #'results': evol_data
            }

        else:
            logger.info('EvolutionView.post: form is invalid')
            logger.info(form.errors)




        return HttpResponse(template.render(context, request))


class PowerUpView(View):
    '''
    This is used to serve requests for the power up calculator.
    '''

    def get(self, request):
        logger.info('PowerUp.get: Enter')

        template = loader.get_template('calculator.html')
        context = {
            'page_title': 'Power Up Calculator',
            'page_description': "This is used to identify a the cost to power up a pokemon"
        }

        return HttpResponse(template.render(context, request))
