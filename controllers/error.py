# -*- coding: UTF-8 -*-


import cgi

from paste.urlparser import PkgResourcesParser
from pylons.middleware import error_document_template
from webhelpers.html.builder import literal

from kd.lib.base import BaseController

ErrorDocumentTemplate = """\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<meta name="language" content="zh_CN" />
	<link rel="stylesheet" type="text/css" href="/css/layout.css" />
	<title>%(code)s</title>
</head>
<body class="home">
<div class="container" id="page">
 <div id="blueBar"> </div>
  <div id="globalContent">
    <div id="pageHead" class="clearfix">
      <h1 id="pageLogo"><a title="Home" href="http://www.kongdai.com/"></a></h1>
      <div id="headNav" class="clearfix">
       
      </div>
    </div>
     %(message)s
  </div>

</div>

</body>
</html>

"""


class ErrorController(BaseController):
    """Generates error documents as and when they are required.

    The ErrorDocuments middleware forwards to ErrorController when error
    related status codes are returned from the application.

    This behaviour can be altered by changing the parameters to the
    ErrorDocuments middleware in your config/middleware.py file.

    """
    def document(self):
        """Render the error document"""
        request = self._py_object.request
        resp = request.environ.get('pylons.original_response')
        content = unicode(resp.body) or cgi.escape(request.GET.get('message', ''))
        page = ErrorDocumentTemplate % \
            dict(prefix=request.environ.get('SCRIPT_NAME', ''),
                 code=unicode(cgi.escape(request.GET.get('code', str(resp.status_int)))),
                 
                 message=content)
        return page

    def img(self, id):
        """Serve Pylons' stock images"""
        return self._serve_file('/'.join(['media/img', id]))

    def style(self, id):
        """Serve Pylons' stock stylesheets"""
        return self._serve_file('/'.join(['media/style', id]))

    def _serve_file(self, path):
        """Call Paste's FileApp (a WSGI application) to serve the file
        at the specified path
        """
        request = self._py_object.request
        request.environ['PATH_INFO'] = '/%s' % path
        return PkgResourcesParser('pylons', 'pylons')(request.environ, self.start_response)
