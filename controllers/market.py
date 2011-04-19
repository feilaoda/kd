import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from kd.lib.base import BaseController, render

log = logging.getLogger(__name__)

class MarketController(BaseController):

    def index(self):
        # Return a rendered template
        #return render('/market.mako')
        # or, return a string
        return render('/market/index.html')


    def category(self, what=None):
        
        return render('/market/category.html')
        
    
    def detail(self):
        return render('/market/detail.html')
        
    

