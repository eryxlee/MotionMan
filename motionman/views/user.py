'''
Created on Aug 31, 2011

@author: eric
'''
import logging

from pyramid.view import view_config
from pyramid.url import route_path
from formencode import Schema, validators

from pyramid.httpexceptions import HTTPFound, HTTPUnauthorized
from pyramid_simpleform import Form
from pyramid_simpleform.renderers import FormRenderer

from motionman.services.user import add_user, load_users, load_user, update_user, delete_user

class UserSchema(Schema):

    filter_extra_fields = True
    allow_extra_fields = True

    email = validators.Email(not_empty=True)
    name = validators.MinLength(2, not_empty=True)
    vote_weight = validators.Int(max=10, not_empty=True)

@view_config(route_name='user_add', renderer='motionman:templates/user/user_add.pt', permission='manage')
def user_add(request):
    form = Form(request, schema=UserSchema)

    if form.validate():

        add_user(form.data.get("name"), form.data.get("email"), form.data.get("vote_weight"))
        return HTTPFound(location=route_path("user_list", request))

    return dict(renderer=FormRenderer(form))

@view_config(route_name='user_list', renderer='motionman:templates/user/user_list.pt', permission='manage')
def user_list(request):
    users = load_users()
    return dict(users = users)

@view_config(route_name='user_edit', renderer='motionman:templates/user/user_edit.pt', permission='manage')
def user_edit(request):
    id = request.matchdict['id']
    user = load_user(id)

    if not user:
        return HTTPUnauthorized()
    
    form = Form(request, schema=UserSchema, obj=user)

    if form.validate():
        update_user(id, form.data.get("name"), form.data.get("email"), 
                    form.data.get("vote_weight"))

        return HTTPFound(location=route_path("user_list", request))

    return dict(renderer=FormRenderer(form))

@view_config(route_name='user_delete', permission='manage')
def user_delete(request):
    id = request.matchdict['id']
    user = load_user(id)

    if not user:
        return HTTPUnauthorized()
    
    delete_user(id)

    return HTTPFound(location=route_path("user_list", request))
