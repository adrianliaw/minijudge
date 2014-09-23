#!/usr/bin/python
# -*- coding: utf-8 -*-

import webapp2
from routes import _routes

app = webapp2.WSGIApplication(_routes, debug=True)
