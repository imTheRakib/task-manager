"""
This file defines the database models
"""
from .common import db, Field, session,T
from pydal.validators import *
import os
from py4web import request

### Define your table below
#
# db.define_table('thing', Field('name'))
#
## always commit your models to avoid problems later
#
# db.commit()

from .common_cid import date_fixed

APP_FOLDER = os.path.dirname(__file__)

def get_user_id():
    return session.get('user_id', '')

cid='CDMS'
#---------------------Start Task Management Tables---------------------
signature=db.Table(db,'signature',
                Field('field1','string',length=100,default=''), 
                Field('field2','integer',default=0),
                Field('note','string',length=255,default=''),  
                Field('created_on','datetime',default=date_fixed),
                Field('created_by',default=get_user_id),
                Field('updated_on','datetime',update=date_fixed),
                Field('updated_by',update=get_user_id),
                
                )

#*******************start role Tables*******************
db.define_table(
    "role",
    Field('cid','string', length=20, default=cid),
    Field("role_id", "integer", length=10),
    Field("role_name", "string", length=200),
    Field("role_description", "text", length=500),
    Field("role_status", 'string', length=50),
    signature,
    migrate=False
)
#*******************end role Tables*******************


#*******************start user Tables*******************
db.define_table(
    "user",
    Field('cid','string', length=20, default=cid),
    Field("user_id", "integer", length=10),
    Field("user_name", "string", length=200),
    Field("user_email", 'string',length=100),
    Field("user_password", "password", length=500),
    Field("user_mobile", "string", length=20),
    signature,
    migrate=False
)
#*******************end user Tables*******************


#*******************start user_role Tables*******************
db.define_table(
    "user_role",
    Field('cid','string', length=20, default=cid),
    Field("user_id", "integer", length=10),
    Field("role_id", "integer", length=10),
    signature,
    migrate=False
)
#*******************end user_role Tables*******************


#*******************start project Tables*******************
db.define_table(
    "project",
    Field('cid','string', length=20, default=cid),
    Field("bu", "string", length=10),
    Field("project", "string", length=20),
    Field("project_descrip", "text", length=500),
    Field("owner", "string", length=20),
    Field("reliever", "string", length=20),
    Field("status", 'string', length=20),
    signature,
    migrate=False
)
#*******************end project Tables*******************

#*******************start module Tables*******************
db.define_table(
    "module",
    Field('cid', 'string', length=20, default=cid),
    Field("bu", "string", length=10),
    Field("project", "string", length=50),
    Field("module", "string", length=200),
    Field("des", "text", length=500),
    Field("owner", "string", length=20),
    Field("reliever", "string", length=20),
    Field("status", "string", length=20),
    signature,
    migrate=False
)
#*******************end module Tables*******************

#*******************start tasks Tables*******************
db.define_table(
    "tasks",
    Field('cid', 'string', length=20, default=cid),
    Field("bu", "string", length=10),
    Field("project", "string", length=50),
    Field("module", "string", length=200),
    Field("task", "string", length=300),
    Field("owner", "string", length=20),
    Field("reliever", "string", length=20),
    Field("task_status", "string", length=20),
    Field("start_date", "date"),
    Field("end_date", "date"),
    Field("priority", "string", length=20),
    Field("description", "text", length=500),
    Field("comments", "text", length=300),
    signature,
    migrate=False
)
#*******************end tasks Tables*******************

#*******************start tasks_log Tables*******************
db.define_table(
    "tasks_log",
    Field('cid', 'string', length=20, default=cid),
    Field("bu", "string", length=10),
    Field("project", "string", length=50),
    Field("module", "string", length=200),
    Field("task", "string", length=300),
    Field("owner", "string", length=20),
    Field("reliever", "string", length=20),
    Field("task_status", "string", length=20),
    Field("start_date", "date"),
    Field("end_date", "date"),
    Field("priority", "string", length=20),
    Field("description", "text", length=500),
    Field("comments", "text", length=300),
    Field("updated_on", "datetime"),
    signature,
    migrate=False
)
#*******************end tasks_log Tables*******************

#*******************start work_log Tables*******************
db.define_table(
    "work_log",
    Field('cid','string', length=20, default=cid),
    Field("emp_id", "integer", length=10),
    Field("work_date", "date"),
    Field("status", "string", length=20),
    Field("work_hours", "double", length=20),
    Field("work_description", "text", length=500),
    Field("related_task_id", "integer", length=20),
    signature,
    migrate=False
)
#*******************end work_log Tables*******************

#---------------------End Task Management Tables---------------------