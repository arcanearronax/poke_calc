from django.http import HttpResponse
from django.views import View
from django.template import loader
import logging

logger = logging.getLogger('baselogger')

class PokeView(View):
    
    def get(self, request, *args, **kwargs):
        logger.info('PokeView.get: Enter')

        template = loader.get_template('base.html')
        context = {
            'message': 'IT WORKS',
        }
        return HttpResponse(template.render(context, request))
