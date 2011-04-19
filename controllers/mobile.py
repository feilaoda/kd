import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from kd.lib.base import BaseController, render
from kd.model.meta import Session
from kd.model.software import Software
from formencode import htmlfill
import formencode
from pylons.decorators import validate

log = logging.getLogger(__name__)


class NewSoftwareForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    software_name = formencode.validators.String(not_empty = True)
    download_url = formencode.validators.String(not_empty = True)
      
      
class MobileController(BaseController):
      
    def index(self):
        softq = Session.query(Software).limit(100)
        c.softs = softq       
        return render('/mobile/index.html')
        
    def add(self):
        return render('/mobile/add.html')
        
    def custom_formatter(error):
        return '<span class="custom-message">%s</span>' % (
            htmlfill.html_quote(error))
            
    @validate(schema=NewSoftwareForm(), form='add',  auto_error_formatter=custom_formatter)
    def doadd(self):
        soft = Software()
        soft.name = self.form_result.get('software_name')
        soft.download_url =  self.form_result.get('download_url')
        Session.add(soft)
        Session.commit()        
        redirect(url(controller="mobile", action="index"))
        
    
                
    def edit(self, id=0):
        soft_id = id
        if soft_id == 0:
            #soft_id = self.form_result.get('software_id')
            redirect(url(controller="mobile", action="index"))        
        soft = Session.query(Software).filter(Software.id == soft_id).first()
        if not soft is None:            
            c.soft = soft
            return render('/mobile/edit.html')        
    
    def _editform(self, id=0):
        return render('/mobile/editform.html')   
    
    @validate(schema=NewSoftwareForm(), form='_editform',  auto_error_formatter=custom_formatter)
    def doedit(self):             
        soft_id = request.params.getone('software_id')  
        soft = Session.query(Software).filter(Software.id == soft_id).first()        
        #soft = Software() #Session.merge(old_soft)
        #soft.id = self.form_result.get('software_id')  
        soft.name = self.form_result.get('software_name')
        soft.download_url =  self.form_result.get('download_url')      
        
        Session.commit()        
        #redirect(url(controller="mobile", action="index"))  
        
        redirect(url(controller="mobile", action="index"))  
            
    def saveSoftware(self, soft):
        Session.query(Software).filter(Software.id == soft.id).update({Software.name: soft.name, Software.download_url: soft.download_url})
            
        Session.commit()
        
    #@validate(schema=NewSoftwareForm(), form='edit',  auto_error_formatter=custom_formatter)
    def doeditX(self, id=0):
        schema = NewSoftwareForm()
        try:
            c.form_result = schema.to_python(dict(request.params))
        except formencode.Invalid, error:
            c.form_result = error.value
            c.form_errors = error.error_dict or {}
            soft_id = id
            if soft_id == 0:
                redirect(url(controller="mobile", action="index"))        
            soft = Session.query(Software).filter(Software.id == soft_id).first()
            #if not soft is None:            
            c.soft = soft
            html = render('/mobile/edit.html')
            return htmlfill.render(
                html,
                defaults=c.form_result,
                errors=c.form_errors
                #auto_error_formatter=self.custom_formatter
            )
        else:              
            soft = Software()
            soft.id = c.form_result.get('software_id')
            soft.name = c.form_result.get('software_name')
            soft.download_url =  c.form_result.get('download_url')
            Session.update(soft)
            Session.commit()        
            redirect(url(controller="mobile", action="index"))     
        

    
#    def newnode(self, id):
#      c.parent_id = id
#      return render('newnode.html')
#    
#    @validate(schema=NewSoftwareForm(), form='add')
#    def createnode(self):
#      soft_name = self.form_result.get('software_name')
#      soft_url = self.form_result.get('download_url')
#      soft_id = save_the_data(parentId, childName)
#      return redirect_to(controller = 'mobile', action = 'index', id = soft_id)
        


