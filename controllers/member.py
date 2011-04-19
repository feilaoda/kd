import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from repoze.what.predicates import not_anonymous, has_permission
from repoze.what.plugins.pylonshq import ActionProtector

from kd.lib.base import BaseController, render

log = logging.getLogger(__name__)

class MemberController(BaseController):

    #todo
    def index(self):
        return render('/member/index.html')
 
    #todo
    def logout(self):
        redirect(url(controller='member', action='index'))
  
    #todo
    def register(self):
        return render('/member/register.html')
 
    #todo
    def login(self):
        """
        This is where the login form should be rendered.
        Without the login counter, we won't be able to tell if the user has
        tried to log in with wrong credentials
        """
        identity = request.environ.get('repoze.who.identity')
        return_url = str(request.GET.get('return_url', '')) or \
                    url(controller='member', action='welcome')
        if identity:
            redirect(url(controller='member', action='welcome'))
        else:
            c.return_url = return_url
            #c.login_counter = request.environ['repoze.who.logins'] + 1
            return render('/member/login.html')
              
              
    def dologin(self):
        redirect(url(controller='member', action='index'))
                      
    


