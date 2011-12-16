'''
Created on Aug 30, 2011

@author: eric
'''
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.url import route_url
from formencode import Schema, validators

from pyramid.httpexceptions import HTTPFound
from pyramid_simpleform import Form
from pyramid_simpleform.renderers import FormRenderer

from motionman.services.setting import *

class SettingSchema(Schema):

    filter_extra_fields = True
    allow_extra_fields = True

    motion_id_prefix = validators.MinLength(2, not_empty=True)

    admin_password = validators.MinLength(5, not_empty=True)
    user_password = validators.MinLength(5, not_empty=True)

    mail_sender = validators.Email(not_empty=True)
    mail_smtppassword = validators.MinLength(5, not_empty=True)
    mail_template = validators.MinLength(5, not_empty=True)
    
class MySetting():
    pass
     
@view_config(route_name='setting_edit', renderer='motionman:templates/setting/setting_form.pt', permission='manage')
def edit(request):
    settings = load_settings()

    my = MySetting()
    for setting in settings:
        if setting.valuex:
            my.__dict__[setting.name] = setting.valuex
        else:
            my.__dict__[setting.name] = setting.value

    form = Form(request,
                schema=SettingSchema,
                obj=my)

    if form.validate():
        form.bind(my)

        # persist model somewhere...
        for setting in settings:
            if setting.name == "motion_id_prefix":
                update_setting(setting.name, my.motion_id_prefix)
            if setting.name == "admin_password":
                update_setting(setting.name, my.admin_password)
            if setting.name == "user_password":
                update_setting(setting.name, my.user_password)
            if setting.name == "mail_sender":
                update_setting(setting.name, my.mail_sender)
            if setting.name == "mail_smtppassword":
                update_setting(setting.name, my.mail_smtppassword)
            if setting.name == "mail_template":
                update_setting(setting.name, "", my.mail_template)
            
            
        return HTTPFound(location=route_url("setting_edit", request))

    return dict(renderer=FormRenderer(form))
    
