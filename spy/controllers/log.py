#!/usr/bin/env python
"""
Tools to help with logging.

Copyright (c) 2008 Dustin Sallings <dustin@spy.net>
"""

import time
import logging

class RequestLogMixin(object):
    """Add this to your bases to log each http method with timings."""

    __HTTP_METHODS=['get', 'post', 'put', 'head', 'delete', 'trace']
    __WRAPS=(['before_' + x for x in __HTTP_METHODS] +
             ['after_' + x for x in __HTTP_METHODS])

    def __init__(self):
        super(RequestLogMixin, self).__init__()
        self.tracked = {}

    def __before(self, method):
        def x(*args): self.tracked[method]=time.time()
        return x

    def __after(self, method):
        def x(*args):
            logging.info("Finished %s.%s in %ss", type(self), method,
                (time.time()-self.tracked[method]))
        return x

    def __getattr__(self, attr):
        if attr in self.__WRAPS:
            if attr.startswith('before_'):
                rv=self.__before(attr.replace("before_", ""))
            else:
                rv=self.__after(attr.replace("after_", ""))
            return rv
        else:
            raise AttributeError(attr)

