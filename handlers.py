#!/usr/bin/python
# -*- coding: utf-8 -*-

import webapp2


class MainHandler(webapp2.RequestHandler):

    def get(self):

        self.response.out.write('hello world')


