#!/usr/bin/python
# -*- coding: utf-8 -*-

import handlers

_routes = [('/', handlers.MainHandler), ('/test',
           handlers.TestHandler), ('/user', handlers.UserHandler),
           ('/minijudge', handlers.MiniJudge)]
