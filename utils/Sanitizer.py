# -*- coding: utf-8 -*-

def put_sanitized(dict, sql):
    for k, v in dict.iteritems():
        setattr(sql, k, v)
