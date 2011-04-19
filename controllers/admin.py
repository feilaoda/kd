import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from formencode import htmlfill
import formencode
from pylons.decorators import validate


from kd.lib.base import BaseController, render

log = logging.getLogger(__name__)

class NewSoftwareForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    Software[name] = formencode.validators.String(not_empty = True)
    Software[download_url] = formencode.validators.String(not_empty = True)
      
      
      
class AdminController(BaseController):

    def index(self):
        # Return a rendered template
        #return render('/admin.mako')
        # or, return a string
        return render('/admin/index.html')
        
    def _new_software(self):
        return 'New software'        
        
    def new_software(self): 
        return render("/admin/new_software.html")
        
  
    def custom_formatter(error):
        return '<span class="custom-message">%s</span>' % (
            htmlfill.html_quote(error))
            
    @validate(schema=NewSoftwareForm(), form='new_software',  auto_error_formatter=custom_formatter)
    def do_new_software(self):
        soft = Software()
        soft.name = self.form_result.get('Software[name]')
        soft.download_url =  self.form_result.get('Software[download_url]')
        
        Session.add(soft)
        Session.commit()        
        redirect(url(controller="admin", action="index"))
        
    def edit(self, what=None, id=None):
        return 'Edit what'

    def upload(self, what=None):
        request.set_field_maxlen('myfile', 1000)
        #request.set_maxlen_safe(True)
        
        return "uploading files..."
        