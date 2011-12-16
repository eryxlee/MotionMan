"""Setup the sso application"""
import logging

#from sso.model import meta
from sqlalchemy import engine_from_config
from motionman.models import initialize_sql

from motionman.models.init_data import init_data

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup sso here"""
#    load_environment(conf.global_conf, conf.local_conf)
    print "command", command
    print "conf", conf
    print "vars", vars
    # Create the tables if they don't already exist
#    meta.metadata.create_all(bind=meta.engine)

    engine = engine_from_config(conf, 'sqlalchemy.')
    initialize_sql(engine)
    
    init_data()
