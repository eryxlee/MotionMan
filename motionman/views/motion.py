'''
Created on Aug 31, 2011

@author: eric
'''

from pyramid.view import view_config
from pyramid.url import route_url

from formencode import Schema, validators, ForEach
from pyramid.httpexceptions import HTTPFound, HTTPUnauthorized, HTTPBadRequest
from pyramid_simpleform import Form
from pyramid_simpleform.renderers import FormRenderer

from motionman.services.user import load_users
from motionman.services.motion import add_motion, load_motions, load_motion
from motionman.services.motion import get_motion_participant_by_chips, save_vote_result
from motionman.services.message import add_message


class MotionSchema(Schema):
    """Motion validate schema
    
    Motion validate schema to assure title is not null 
    options is a motion options list containing all options description.
    participants is user id list of all users allowed to vote on this motion.
    """

    filter_extra_fields = True
    allow_extra_fields = True

    title = validators.MinLength(2, not_empty=True)
    desc = validators.String()

    options = ForEach(validators.String())
    participants = ForEach(validators.Int())

@view_config(route_name='motion_add', renderer='motionman:templates/motion/motion_add.pt')
def motion_add(request):
    """create a new motion.
    
    1. show new motion form
    2. save to database after user submit
    """
    
    # initialize the form to select all participants
    all_users = load_users()
    all_user_options = [(itm.id, itm.name) for itm in all_users]
    selected_users = [itm.id for itm in all_users]

    # add four blank options on new motion form
    form = Form(request, schema=MotionSchema, defaults=dict(participants = selected_users, 
                                                            options=["","","",""]))
    
    if form.validate():
        title = form.data.get("title")
        desc = form.data.get("desc")
        options = form.data.get("options")
        users = form.data.get("participants")

        add_motion(title, desc, options, users)

        return HTTPFound(location=route_url('motion_list', request))
        
    return dict(renderer=FormRenderer(form), all_user_options=all_user_options)

@view_config(route_name='motion_list', renderer='motionman:templates/motion/motion_list.pt')
@view_config(route_name='home', renderer='motionman:templates/motion/motion_list.pt')
def motion_list(request):
    return dict(motions = load_motions())

@view_config(route_name='motion_vote', renderer='motionman:templates/motion/motion_vote.pt')
def motion_vote(request):
    motion_id = request.matchdict['id']
    chips = request.matchdict['chips']
    
    motion = load_motion(motion_id)
    if not motion:
        return HTTPBadRequest()

    #validate chips exists and not used
    participant = get_motion_participant_by_chips(motion.id, chips)
    if not participant:
        return HTTPUnauthorized()

    if request.params.get('submit'):
        vote_result = request.params.get("vote")
        save_vote_result(motion_id, vote_result, chips)
        return HTTPFound(location=route_url('motion_vote', request, 
                                                id=motion_id, chips=chips))
    
    return dict(motion=motion, participant=participant)

@view_config(route_name='motion_message', renderer='motionman:templates/motion/motion_message.pt')
def motion_message(request):
    motion_id = request.matchdict['id']
    
    motion = load_motion(motion_id)
    if not motion:
        return HTTPBadRequest()

    if request.params.get('submit') and request.params.get("message"):
        message = request.params.get("message").strip()
        if message:
            add_message(motion_id, message)

    return dict(motion=motion)
