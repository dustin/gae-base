#!/usr/bin/env python
"""
My app's controllers.

Copyright (c) 2008 Dustin Sallings <dustin@spy.net>
"""
import logging

import spy.controllers

class MainHandler(spy.controllers.BaseHandler,
                  spy.controllers.RequestLogMixin):

    def get(self):
        logging.info("Look, I'm in method %s", self.currentMethod)
        self.renderTemplate('index.html')
