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


@view_config(route_name='message_list', renderer='motionman:templates/message/message.pt')
def message_list(request):
    motion_id = request.matchdict['id']
    
    motion = load_motion(motion_id)
    if not motion:
        return HTTPBadRequest()

    return dict(motions = load_motions())

