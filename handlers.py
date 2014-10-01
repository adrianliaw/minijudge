#!/usr/bin/python
# -*- coding: utf-8 -*-

import webapp2
from jinja2 import Environment, FileSystemLoader
from google.appengine.api import users
from google.appengine.ext import ndb
from webapp2_extras.appengine.users import *
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

    def nickname(self):
        user = users.get_current_user()
        if user:
            return user.nickname()
        else:
            return 'fella'


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

    @login_required
    def get(self):
        self.render('minijudge.html', nickname=self.nickname())

    def post(self):

        sucess = False

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
                    sucess = True
                elif code == 404:
                    msg = 'Sorry, 404 girlfriend not found on %s.' % url
                else:
                    msg = 'we encounter some tough situation.%s' % code
            except:
                msg = 'we encounter some tough situation.'
        else:
            msg = 'no url input.'
        self.render('minijudge.html', msg=msg, nickname=self.nickname())

        if sucess:
            print 'url ping sucess'
            user = users.get_current_user()
            if user:
                uid = user.user_id()
                q = ndb.gql('SELECT * FROM User WHERE uid = :1', uid)
                u = q.get()
                if u:
                    print 'This user already stored in db, here it is %s' \
                        % u
                    self.redirect('/')
                else:
                    print 'This user is not yet in db, storing now'
                    new_u = User.register(uid=uid,
                            name=user.nickname(), site=url,
                            is_success=True)
                    new_u.put()
                    self.redirect('/')


class User(ndb.Model):

    uid = ndb.StringProperty(required=True)
    name = ndb.StringProperty()
    site = ndb.StringProperty()
    is_success = ndb.BooleanProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def by_id(cls, uid):
        return User.get_by_id(uid, parent=users_key())

#    @classmethod
#    def by_name(cls, name):
#        u = User.all().filter('name =', name).get()
#        return u
#

    @classmethod
    def register(
        cls,
        uid,
        name='',
        site='',
        is_success=False,
        ):

        return User(uid=uid, name=name, site=site,
                    is_success=is_success)

        @classmethod
    def query_all(cls):
        return cls.query().order(-cls.created)

    @classmethod
    def query_all(cls):
        return cls.query().order(-cls.created)


#
#    @classmethod
#    def login(cls, name, pw):
#        u = cls.by_name(name)
#        if u and valid_pw(name, pw, u.pw_hash):
#            return u

#        u = User.by_name(self.username)
#        if u:
#            msg = 'The user already exists.'
#            self.write('signup.html', user_error=msg)
#        else:
#            u = User.register(self.username, self.password, self.email)
#        u.put()
#
#        self.login(u)
#        self.redirect('/welcome')

class DashBoard(BaseHandler):

    def get(self):
        users = User.query_all()
        self.render('dashboard.html', users=users)


