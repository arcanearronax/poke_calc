from django import template
import logging

register = template.Library()
logger = logging.getLogger('baselogger')

@register.filter(name='get_row_data')
def get_row_data(evol_data):
    #logger.info('show_tags.match_found_processer: {}'.format(data_point))
    row_data = [[] * next(iter(evol_data.values()))['min_value']]
    logger.info('show_tags: found min_level={}'.format(next(iter(evol_data.values()))['min_value']))

    for pokemon in evol_data:
        pass
