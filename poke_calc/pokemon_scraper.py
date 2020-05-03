from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import logging

logger = logging.getLogger('baselogger')

class PokemonStatsScraper():
    '''
    This class is used to request individual pokemon stats ffrom pokemongohub.
    '''
    base_url = 'https://db.pokemongohub.net/pokemon/{}/iv-chart?level={}'

    def get_stats(dex_num, level, form=''):
        logger.info('PokemonStatsScraper.get_stats: {} - {} - {}'.format(dex_num, level, form))

        assert form in ('', 'Alola'), 'Invalid form provided: {}'.format(form)

        # Build our request's URL
        if form:
            req_url = '{}&form={}'.format(PokemonStatsScraper.base_url.format(dex_num, level), form)
        else:
            req_url = PokemonStatsScraper.base_url.format(dex_num, level)

        # Open the browser window
        driver = webdriver.Firefox()
        driver.get(req_url)

        # Find the button
        driver.find_elements_by_xpath('//button[text()="Next"]')[0]
        logger.info('Found the button')

        # Need to create an array of pages to read data from
        for _ in range(82):

            # Create a soup object with the page source
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            logger.info('Created a page')

            # Find the values in each row on the page
            divs = soup.find_all('div', {'class': 'rt-tr-group'})

            for div in divs:
                logger.info('Finding Values')
                # Get the values in the rows
                cp = divs.find('div', {'class': 'rt-td'}).text
                logger.info('FOUND VALUE: {}'.format(cp))
                indiv_atk
                indiv_def
                indiv_sta

            # Locate the button

            # Click the button
