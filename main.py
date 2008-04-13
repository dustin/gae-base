#!/usr/bin/env python

import time

import wsgiref.handlers

from google.appengine.ext import webapp

import controllers

def main():
    application = webapp.WSGIApplication([
        ('/', controllers.MainHandler),
        ], debug=True)
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
    main()
