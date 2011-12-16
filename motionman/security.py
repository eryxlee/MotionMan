USERS = {'editor':'editor',
         'viewer':'viewer',
         'admin':'admin'}
GROUPS = {'editor':['group:editors'], 'admin':['group:admins']}

def groupfinder(userid, request):
    if userid in USERS:
        return GROUPS.get(userid, [])

