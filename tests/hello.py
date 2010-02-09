# -*- coding: utf-8 -*-

def index():
    return unicode('index')

def new():
    return unicode('new')

def create():
    return unicode('create')

def show(id):
    return unicode('show %s' % str(id))

def edit(id):
    return unicode('edit %s' % str(id))

def update(id):
    return unicode('update %s' % str(id))

def delete(id):
    return unicode('delete %s' % str(id))

def sweet():
    return unicode('sweet')
