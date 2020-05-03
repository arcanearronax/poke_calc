from django.db import models
from .pokemon_scraper import PokemonStatsScraper
import logging

logger = logging.getLogger('baselogger')

class Pokemon(models.Model):
    '''
    This is the Pokemon model. It holds information true for all pokemon.
    '''
    pokemon_id = models.IntegerField(primary_key=True)
    dex_num = models.IntegerField()
    pokemon_name = models.CharField(max_length=100)
    base_atk = models.IntegerField()
    base_def = models.IntegerField()
    base_sta = models.IntegerField()
    aloan = models.NullBooleanField(default=False)
    galarian = models.NullBooleanField(default=False)

    @classmethod
    def get_by_name(cls, pokemon_name):
        '''
        This returns a pokemon based on the search name provided
        '''
        logger.info('Pokemon.get_by_name: {}'.format(pokemon_name))

        try:
            return cls.objects.filter(pokemon_name=pokemon_name)[0]
        except Exception as e:
            logger.info('EXCEPTION: {}'.format(e))
            return None

    def get_name(self):
        return self.pokemon_name

    def get_base_atk(self):
        return self.base_atk

    def get_base_def(self):
        return self.base_def

    def get_base_sta(self):
        return self.base_sta

    def get_dex_num(self):
        return self.dex_num

    @classmethod
    def create():
        '''
        This is used to create new Pokemon entries
        '''
        pass

class PokemonStats(models.Model):
    '''
    This holds pokemon stats with their associated level.
    '''
    pokemon_id = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    level = models.IntegerField()
    cp = models.IntegerField()
    indiv_atk = models.IntegerField()
    indiv_def = models.IntegerField()
    indiv_sta = models.IntegerField()

    @classmethod
    def get_entries_by_level(cls, pokemon_id,level):
        '''
        This returns an array of dictionary objects containing individual values
        and related stats for pokemon.
        '''
        logger.info('PokemonStats.get_entries_by_level: {} - {}'.format(pokemon_id, level))

        try:
            return cls.objects.filter(pokemon_id=pokemon_id, level=level)
        except Exception as e:
            logger.info('PokemonStats.get_entries_by_level EXCEPTION: {}'.format(e))
            return None


    @classmethod
    def create():
        '''
        This is used to create new Pokemon Stat entries.
        '''
        pass
