from bs4 import BeautifulSoup
import requests
import logging

logger = logging.getLogger('baselogger')

class PokemonScraper():
    '''
    This class is used to request individual pokemon stats from pokemongohub.
    '''
    base_url = 'https://db.pokemongohub.net/pokemon/{}'

    def get_base_stats(dex_num, level, form=''):
        logger.info('PokemonStatsScraper.get_stats: {} - {} - {}'.format(dex_num, level, form))

        assert form in ('', 'Alola'), 'Invalid form provided: {}'.format(form)

        # Build our request's URL
        if form:
            req_url = '{}&form={}'.format(PokemonStatsScraper.base_url.format(dex_num, level), form)
        else:
            req_url = PokemonStatsScraper.base_url.format(dex_num, level)

        # Get the pokemon's page
        req = requests.get(req_url)
        assert req.status_code == 200, 'Failed to retrieve page: {}'.format(req.status_code)

        # Get the entries from the page
        soup = BeautifulSoup(req.content, 'html.parser')
        stat_table = soup.find('table', {'class': 'pokemon--stats'})
        stat_tbody = stat_table.find('tbody')
        stat_values = stat_tbody.find_all('td')

        # Parse out the identified entries
        base_atk = stat_values[1].text
        base_def = stat_values[2].text
        base_sta = stat_values[3].text

        # Return a dict with the base stats
        return {
            'base_atk': base_atk,
            'base_def': base_def,
            'base_sta': base_sta,
        }
