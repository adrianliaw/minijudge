#!/usr/bin/python
# -*- coding: utf-8 -*-

import webapp2
from jinja2 import Environment, FileSystemLoader
from google.appengine.api import users
import urllib2
import cgi


class MainHandler(webapp2.RequestHandler):

    def get(self):

        self.response.out.write('hello world')


class BaseHandler(webapp2.RequestHandler):

    def render(self, filename, **template_values):
        jinja_env = Environment(loader=FileSystemLoader('templates'))
        template = jinja_env.get_template(filename)
        self.response.out.write(template.render(template_values))


class TestHandler(BaseHandler):

    def get(self):
        self.render('test.html')


class UserHandler(BaseHandler):

    def get(self):
        user = users.get_current_user()

        if user:
            self.render('user.html', msg='Hello, ' + user.nickname())
        else:
            self.redirect(users.create_login_url(self.request.uri))


class MiniJudge(BaseHandler):

    def get(self):
        self.render('minijudge.html')

    def post(self):
        url = self.request.get('inputURL')

        msg = ''
        if url:
            url = cgi.escape(url)
            print url
            try:
                u = urllib2.urlopen(url)

                # see if 200 or 404

                code = u.getcode()
                if code == 200:
                    msg = 'Congrat! we ping %s sucessfully.' % url
                elif code == 404:
                    msg = 'Sorry, 404 girlfriend not found on %s.' % url
                else:
                    msg = 'we encounter some tough situation.%s' % code
            except:
                msg = 'we encounter some tough situation.'
        else:
            msg = 'no url input.'
        self.render('minijudge.html', msg=msg)


