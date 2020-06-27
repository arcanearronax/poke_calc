from django.http import HttpResponse
from django.views import View
from django.template import loader
from .models import Pokemon, PokemonStats, Evolution, CPMultiplier
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
            poke_id = form.cleaned_data['pokemon']
            indiv_atk = form.cleaned_data['indiv_atk']
            indiv_def = form.cleaned_data['indiv_def']
            indiv_sta = form.cleaned_data['indiv_sta']
            cp = form.cleaned_data['cp']

            request.session['pokemon'] = poke_id
            request.session['indiv_atk'] = indiv_atk
            request.session['indiv_def'] = indiv_def
            request.session['indiv_sta'] = indiv_sta
            request.session['cp'] = cp

            logger.info('SESSION_DATA: {}'.format(request.session['cp']))

            # Get the pokemon's poke_id
            logger.info('The form says: {} {} {} {} {}'.format(poke_id, indiv_atk, indiv_def, indiv_sta, cp))
            logger.info('Pokemon: {}'.format(poke_id))

            # Get provided pokemon's level
            pokemon = Pokemon.get_by_poke_id(poke_id)
            level = PokemonStats.calculate_level(pokemon, indiv_atk, indiv_def, indiv_sta, cp)
            logger.info('Got level: {}'.format(level))

            # Identify the possible evolutions
            poke_list = Evolution.get_evolutions(poke_id)
            logger.info('POKE_LIST: {}'.format(poke_list))

            # Get the possible cp values for the evolutions
            evol_cp = {
                str(evol.get_poke_id()): CPMultiplier.get_cp_values(evol, indiv_atk, indiv_def, indiv_sta, min_level=level) for evol in poke_list
            }

            # Prep the data for our table
            evol_data = {
                str(Pokemon.get_by_poke_id(k).get_name()): v for k,v in evol_cp.items()
            }

            logger.info('EVOL_DATA: {}'.format(evol_data))

            template = loader.get_template('calculator.html')
            context = {
                'page_title': 'Evolution Calculator',
                'page_description': "Here are the pokemon's results",
                'form': EvolutionForm(initial={
                    'pokemon': request.session.get('pokemon'),
                    'indiv_atk': request.session.get('indiv_atk'),
                    'indiv_def': request.session.get('indiv_def'),
                    'indiv_sta': request.session.get('indiv_sta'),
                    'cp': request.session.get('cp'),
                    }),
                'evol_data': evol_data
            }

        else:
            logger.info('EvolutionView.post: form is invalid')
            logger.info(form.errors)
            template = loader.get_template('calculator.html')
            context = {
                'page_title': 'Evolution Calculator',
                'page_description': "You got an error",
                'form': EvolutionForm(),
                #'results': evol_data
            }



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
