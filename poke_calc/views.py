from django.http import HttpResponse
from django.views import View
from django.template import loader
from .models import Pokemon
from .pokemon_scraper import PokemonStatsScraper
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

class PokemonStatsView(View):
    '''
    This is used to serve requests for pokemon stats.
    '''

    def get(self, request, pokemon_name, level):
        logger.info('PokemonStatsView.get: {}'.format(pokemon_name))

        template = loader.get_template('pokemon_stats.html')
        logger.info('found: {}'.format(pokemon_name))
        pokemon = Pokemon.get_by_name(pokemon_name)

        # Need to use the scraper to pull data
        entries = PokemonStatsScraper.get_stats(pokemon.get_dex_num(), level)

        context = {
            'pokemon_name': pokemon.get_name(),
            'entries': entries,
        }

        return HttpResponse(template.render(context, request))
