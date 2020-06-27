from django.db import models
from .pokemon_scraper import PokemonScraper
import logging

logger = logging.getLogger('baselogger')

class Pokemon(models.Model):
    '''
    This is the Pokemon model. It holds information true for all pokemon.
    '''
    poke_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    dex_id = models.IntegerField()
    form = models.CharField(max_length=20, null=True)

    def __str__(self):
        return '{}'.format({
            'poke_id': self.get_poke_id(),
            'name': self.get_name(),
            'dex_id': self.get_dex_id(),
            'form': self.get_form(),
        })

    @classmethod
    def get_by_name(cls, pokemon_name):
        '''
        This returns a pokemon based on an exact name match
        '''
        logger.info('Pokemon.get_by_name: {}'.format(pokemon_name))

        try:
            return cls.objects.filter(name=pokemon_name)[0]
        except Exception as e:
            logger.info('EXCEPTION: {}'.format(e))
            return None

    @classmethod
    def get_by_poke_id(cls, poke_id):
        '''
        This returns a pokemon based on their primary key.
        '''
        logger.info('Pokemon.get_by_poke_id: {}'.format(poke_id))

        try:
            return cls.objects.get(poke_id=poke_id)
        except Exception as e:
            logger.info('poke_id error: {}'.format(e))

    def get_poke_id(self):
        return self.poke_id

    def get_name(self):
        return self.name

    def get_dex_id(self):
        return self.dex_id

    def get_form(self):
        return self.form

    @classmethod
    def create():
        '''
        This is used to create new Pokemon entries
        '''
        raise NotImplementedError('Currently not supported')

class PokemonStats(models.Model):
    '''
    This holds pokemon stats with their associated level.
    '''
    poke = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    base_atk = models.IntegerField()
    base_def = models.IntegerField()
    base_sta = models.IntegerField()

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
    def get_atk(cls, pokemon):
        return cls.objects.get(poke=pokemon).base_atk

    @classmethod
    def get_def(cls, pokemon):
        return cls.objects.get(poke=pokemon).base_def

    @classmethod
    def get_sta(cls, pokemon):
        return cls.objects.get(poke=pokemon).base_sta

    @classmethod
    def validate_cp(cls, pokemon, indiv_atk, indiv_def, indiv_sta, cp):
        '''
        This returns the level of a pokemon with the given cp, raises an error
        if the cp isn't found
        '''
        logger.info('cls.validate_cp: Enter - {}'.format(cp))
        cp_values = CPMultiplier.get_cp_values(pokemon, indiv_atk, indiv_def, indiv_sta)
        # Just going to make this work...
        for v in cp_values['values']:
            if v == cp:
                return float(cp_values['values'].index(v) * 0.5 + cp_values['min_level'] + 1)

        # Now we failed to find a match
        raise Exception('Value not found')

    @classmethod
    def calculate_level(cls, pokemon, indiv_atk, indiv_def, indiv_sta, cp):
        '''
        This is used to determine if a pokemon's individual stats
        can produce a given cp
        '''
        return cls.validate_cp(pokemon, indiv_atk, indiv_def, indiv_sta, cp)

class Evolution(models.Model):
    '''
    This holds the various pokemon evolutions.
    '''

    QUERY = """
        WITH RECURSIVE cte AS (
            SELECT p.poke_id, p.evolution_id, 1 AS level
            FROM   (
                SELECT p.poke_id, e.evolution_id
                FROM   poke_calc_pokemon p
                LEFT JOIN   poke_calc_evolution e
                    ON p.poke_id = e.poke_id) p
            WHERE  p.poke_id = {}

            UNION  ALL
            SELECT p.poke_id, p.evolution_id, c.level + 1
            FROM   cte c
            JOIN   (
                SELECT p.poke_id, e.evolution_id
                FROM   poke_calc_pokemon p
                LEFT JOIN   poke_calc_evolution e
                    ON p.poke_id = e.poke_id) p
                ON c.evolution_id = p.poke_id
        )
        SELECT DISTINCT poke_id
        FROM   cte
        ORDER  BY poke_id;
    """

    id = models.IntegerField(primary_key=True)
    poke = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='pre')
    evolution = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='post')

    def __str__(self):
        return '({}, {})'.format(self.get_poke_id(),self.get_evolution())

    def get_poke_id(self):
        '''
        This returns the primary key for the pokemon to evolve.
        '''
        return self.poke

    def get_evolution(self):
        '''
        This returns the primary key for the pokemon to evolve.
        '''
        return self.evolution

    @classmethod
    def get_evolutions(cls, poke_id):
        '''
        This returns an array of pokemon ids that the provided pokemon id can
        evolve into.
        '''
        logger.info('Evolution.get_evolutions: {}'.format(poke_id))
        return [x for x in Pokemon.objects.raw(cls.QUERY.format(poke_id))]

class CPMultiplier(models.Model):
    '''
    This holds the cp multiplier values for stat calculations.
    '''

    level = models.FloatField()
    multiplier = models.FloatField()

    @classmethod
    def get_values(cls):
        return [x for x in cls.objects.all()]

    @classmethod
    def get_cp_values(cls, pokemon, indiv_atk, indiv_def, indiv_sta, min_level=0):
        '''
        This calculates a pokemon's cp at every level, for given individual
        stats.
        '''
        logger.info('CPMultiplier.get_cp_list: {} {} {}'.format(indiv_atk, indiv_def, indiv_sta))

        stamina = PokemonStats.get_sta(pokemon) + indiv_sta
        attack = PokemonStats.get_atk(pokemon) + indiv_atk
        defense = PokemonStats.get_def(pokemon) + indiv_def

        tmp_val = (stamina ** 0.5) * attack * (defense ** 0.5) / 10
        #cp_list = [max(int(tmp_val * (x.multiplier ** 2)), 10) for x in cls.objects.all().order_by('level')]

        logger.info('---TEST ME: {}'.format(cls.objects.filter(level__gte=min_level)))

        cp_values = {
            'min_level': min_level,
            'values': [max(int(tmp_val * (x.multiplier ** 2)), 10) for x in cls.objects.filter(level__gte=min_level).order_by('level')],
        }
        logger.info(cp_values)

        return cp_values

    @classmethod
    def get_cp(cls, pokemon, indiv_atk, indiv_def, indiv_sta, level):
        '''
        This is used to calculate a pokemon's cp at a given level.
        '''
        logger.info('CPMultiplier.get_cp: {} {} {} {}'.format(indiv_atk, indiv_def, indiv_sta, level))

        stamina = PokemonStats.get_sta(pokemon) + indiv_sta
        attack = PokemonStats.get_atk(pokemon) + indiv_atk
        defense = PokemonStats.get_def(pokemon) + indiv_def

        tmp_val = (stamina ** 0.5) * attack * (defense ** 0.5) / 10
        cp = max(int(tmp_val * (cls.filter(level=level)[0].multiplier ** 2)), 10)

        return cp

    @classmethod
    def get_ideal_levels(cls, pokemon, indiv_atk, indiv_def, indiv_sta, level):
        '''
        This is used to identify the
        '''
