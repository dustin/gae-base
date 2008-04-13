import os
import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import models

TEMPLATES = os.path.join(os.path.dirname(__file__), '..', '..', 'templates')

# Created classes
_handlers = {}

class BaseHandlerMeta(type):
    """This metaclass generates and installs filter methods."""

    def __new__(cls, name, bases, attrs):
        # If this isn't a subclass of BaseHandler, don't do anything special.
        if name == 'BaseHandler' or not [c for c in bases if issubclass(c, BaseHandler)]:
            return super(BaseHandlerMeta, cls).__new__(
                cls, name, bases, attrs)

        fqn = attrs['__module__'] + "." + name
        if _handlers.has_key(fqn):
            return _handlers[fqn]

        # Intercept all methods and add a before_x and after_x method.
        for k,v in attrs.items():
            if callable(v) and not (k.startswith('before_') or k.startswith('after_')):

                def wrapper(s):
                    getattr(s, 'before_' + k, lambda *args: None)()
                    s.currentMethod = k
                    v(s)
                    del s.currentMethod
                    getattr(s, 'after_' + k, lambda *args: None)()

                attrs[k] = wrapper

        new_class = type.__new__(cls, name, bases, attrs)
        logging.debug("Created a %s/%s/%s/%s as %s",
            str(cls), str(name), str(bases), str(attrs), str(new_class))

        _handlers[fqn] = new_class
        return _handlers[fqn]        

        def __makeWrappedMethod(methodName, originalMethod):
            return wrapper

class BaseHandler(webapp.RequestHandler):
    """Base class for all of your controllers."""

    __metaclass__ = BaseHandlerMeta

    def renderTemplate(self, name, args={}):
        """Render the given named template under templates/"""
        path = os.path.join(TEMPLATES, name)
        self.response.out.write(template.render(path, args))
