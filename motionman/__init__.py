from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from motionman.models import initialize_sql
from motionman.security import groupfinder

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine)
    
    authn_policy = AuthTktAuthenticationPolicy(
        'sosecret', callback=groupfinder)
    authz_policy = ACLAuthorizationPolicy()
    config = Configurator(settings=settings,
                          root_factory='motionman.models.RootFactory',
                          authentication_policy=authn_policy,
                          authorization_policy=authz_policy)
    
    #config = Configurator(settings=settings)
    config.add_static_view('static', 'motionman:static')
    config.add_route('home', '/')

    config.add_route('setting_edit', '/setting/edit')

    config.add_route('user_list', '/user/list')
    config.add_route('user_add', '/user/add')
    config.add_route('user_edit', '/user/edit/{id}')
    config.add_route('user_delete', '/user/delete/{id}')
    
    config.add_route('motion_list', '/motion/list')
    config.add_route('motion_add', '/motion/add')
    config.add_route('motion_vote', '/motion/vote/{id}/{chips}')
    config.add_route('motion_message', '/motion/message/{id}')

    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

    config.add_view('motionman.views.login.login',
                    context='pyramid.httpexceptions.HTTPForbidden',
                    renderer='motionman:templates/login.pt')
    
    config.scan('motionman.views')

    return config.make_wsgi_app()

