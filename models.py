"""
This file defines the database models for the taskManager app.
Hardened with references, validators, and audit fields for production use.
"""

import os

from pydal.validators import (
    IS_DATE,
    IS_EMAIL,
    IS_EMPTY_OR,
    IS_FLOAT_IN_RANGE,
    IS_IN_DB,
    IS_IN_SET,
    IS_MATCH,
    IS_NOT_EMPTY,
)
from py4web import request

from .common import Field, T, db, session
from .common_cid import date_fixed

APP_FOLDER = os.path.dirname(__file__)


def get_user_id():
    return session.get("user_id", "")


cid = "CDMS"

# Reusable enums
ROLE_STATUS = ["active", "disabled"]
PROJECT_STATUS = ["planned", "in_progress", "blocked", "done", "archived"]
TASK_STATUS = ["todo", "in_progress", "blocked", "in_review", "done", "archived"]
PRIORITY_LEVELS = ["low", "normal", "high", "urgent"]
WORK_LOG_STATUS = ["logged", "approved", "rejected"]
SUBTASK_STATUS = TASK_STATUS
COMMENT_VISIBILITY = ["internal", "external"]

# Shared audit fields
signature = db.Table(
    db,
    "signature",
    Field("field1", "string", length=100, default=""),
    Field("field2", "integer", default=0),
    Field("note", "string", length=255, default=""),
    Field("created_on", "datetime", default=date_fixed),
    Field("created_by", default=get_user_id),
    Field("updated_on", "datetime", update=date_fixed),
    Field("updated_by", update=get_user_id),
)

# --------------------- Start Task Management Tables ---------------------

# Roles
db.define_table(
    "role",
    Field("cid", "string", length=20, default=cid, requires=IS_NOT_EMPTY()),
    Field("name", "string", length=200, requires=IS_NOT_EMPTY(), unique=True),
    Field("description", "text", length=500, default=""),
    Field(
        "status",
        "string",
        length=50,
        default="active",
        requires=IS_IN_SET(ROLE_STATUS),
    ),
    signature,
    migrate=False,
)

# Users
db.define_table(
    "user",
    Field("cid", "string", length=20, default=cid, requires=IS_NOT_EMPTY()),
    Field(
        "email",
        "string",
        length=200,
        requires=[IS_NOT_EMPTY(), IS_EMAIL()],
        unique=True,
    ),
    Field("full_name", "string", length=200, requires=IS_NOT_EMPTY()),
    Field("password", "password", length=512, requires=IS_NOT_EMPTY()),
    Field(
        "mobile",
        "string",
        length=20,
        default=None,
        requires=IS_EMPTY_OR(
            IS_MATCH("^[0-9+\\-]{7,15}$", error_message="Enter 7-15 digits/+/-")
        ),
    ),
    Field(
        "status",
        "string",
        length=20,
        default="active",
        requires=IS_IN_SET(ROLE_STATUS),
    ),
    Field("timezone", "string", length=64, default="UTC"),
    signature,
    migrate=False,
)

# User to role mapping
db.define_table(
    "user_role",
    Field("cid", "string", length=20, default=cid, requires=IS_NOT_EMPTY()),
    Field(
        "user_id",
        "reference user",
        requires=IS_IN_DB(db, "user.id", "%(email)s"),
        ondelete="CASCADE",
    ),
    Field(
        "role_id",
        "reference role",
        requires=IS_IN_DB(db, "role.id", "%(name)s"),
        ondelete="CASCADE",
    ),
    Field(
        "unique_pair",
        "string",
        length=128,
        compute=lambda row: f"{row.user_id}:{row.role_id}",
        unique=True,
        readable=False,
        writable=False,
    ),
    signature,
    migrate=False,
)

# Projects
db.define_table(
    "project",
    Field("cid", "string", length=20, default=cid, requires=IS_NOT_EMPTY()),
    Field("bu", "string", length=10, requires=IS_NOT_EMPTY()),
    Field("name", "string", length=120, requires=IS_NOT_EMPTY()),
    Field("description", "text", length=500, default=""),
    Field("owner_id", "string", length=100,),
    Field("reliever_id","string", ),
    Field("status","string",length=20, default="planned",
        #    requires=IS_IN_SET(PROJECT_STATUS),
    ),
    signature,
    migrate=False,
)

# Modules
db.define_table(
    "module",
    Field("cid", "string", length=20, default=cid, requires=IS_NOT_EMPTY()),
    Field("bu", "string", length=10, requires=IS_NOT_EMPTY()),
    Field(
        "project_id",
        "reference project",
        requires=IS_IN_DB(db, "project.id", "%(name)s"),
        ondelete="CASCADE",
    ),
    Field("name", "string", length=200, requires=IS_NOT_EMPTY()),
    Field("description", "text", length=500, default=""),
    Field(
        "owner_id",
        "reference user",
        requires=IS_IN_DB(db, "user.id", "%(email)s"),
    ),
    Field(
        "reliever_id",
        "reference user",
        requires=IS_EMPTY_OR(IS_IN_DB(db, "user.id", "%(email)s")),
    ),
    Field(
        "status",
        "string",
        length=20,
        default="planned",
        requires=IS_IN_SET(PROJECT_STATUS),
    ),
    signature,
    migrate=False,
)

# Tasks
db.define_table(
    "tasks",
    Field("cid", "string", length=20, default=cid, requires=IS_NOT_EMPTY()),
    Field("bu", "string", length=10, requires=IS_NOT_EMPTY()),
    Field(
        "project_id",
        "reference project",
        requires=IS_IN_DB(db, "project.id", "%(name)s"),
        ondelete="CASCADE",
    ),
    Field(
        "module_id",
        "reference module",
        requires=IS_EMPTY_OR(IS_IN_DB(db, "module.id", "%(name)s")),
        ondelete="SET NULL",
    ),
    Field("task", "string", length=300, requires=IS_NOT_EMPTY()),
    Field(
        "owner_id",
        "reference user",
        requires=IS_IN_DB(db, "user.id", "%(email)s"),
    ),
    Field(
        "reliever_id",
        "reference user",
        requires=IS_EMPTY_OR(IS_IN_DB(db, "user.id", "%(email)s")),
    ),
    Field(
        "task_status",
        "string",
        length=20,
        default="todo",
        requires=IS_IN_SET(TASK_STATUS),
    ),
    Field("start_date", "date", requires=IS_DATE()),
    Field("end_date", "date", requires=IS_EMPTY_OR(IS_DATE())),
    Field(
        "priority",
        "string",
        length=20,
        default="normal",
        requires=IS_IN_SET(PRIORITY_LEVELS),
    ),
    Field("description", "text", length=500, default=""),
    Field("comments", "text", length=300, default=""),
    signature,
    migrate=False,
)

# Task change log
db.define_table(
    "tasks_log",
    Field("cid", "string", length=20, default=cid, requires=IS_NOT_EMPTY()),
    Field(
        "task_id",
        "reference tasks",
        requires=IS_IN_DB(db, "tasks.id", "%(task)s"),
        ondelete="CASCADE",
    ),
    Field(
        "from_status",
        "string",
        length=20,
        default="todo",
        requires=IS_IN_SET(TASK_STATUS),
    ),
    Field(
        "to_status",
        "string",
        length=20,
        default="todo",
        requires=IS_IN_SET(TASK_STATUS),
    ),
    Field(
        "changed_by",
        "reference user",
        requires=IS_IN_DB(db, "user.id", "%(email)s"),
    ),
    Field("note", "text", length=500, default=""),
    Field("changed_on", "datetime", default=date_fixed),
    signature,
    migrate=False,
)

# Task assignees (support multi-user assignment)
db.define_table(
    "task_assignee",
    Field("cid", "string", length=20, default=cid, requires=IS_NOT_EMPTY()),
    Field(
        "task_id",
        "reference tasks",
        requires=IS_IN_DB(db, "tasks.id", "%(task)s"),
        ondelete="CASCADE",
    ),
    Field(
        "user_id",
        "reference user",
        requires=IS_IN_DB(db, "user.id", "%(email)s"),
        ondelete="CASCADE",
    ),
    Field(
        "role",
        "string",
        length=50,
        default="assignee",
        requires=IS_IN_SET(["owner", "assignee", "reviewer", "observer"]),
    ),
    Field(
        "unique_pair",
        "string",
        length=128,
        compute=lambda row: f"{row.task_id}:{row.user_id}",
        unique=True,
        readable=False,
        writable=False,
    ),
    signature,
    migrate=False,
)

# Subtasks
db.define_table(
    "task_subtask",
    Field("cid", "string", length=20, default=cid, requires=IS_NOT_EMPTY()),
    Field(
        "parent_task_id",
        "reference tasks",
        requires=IS_IN_DB(db, "tasks.id", "%(task)s"),
        ondelete="CASCADE",
    ),
    Field("title", "string", length=200, requires=IS_NOT_EMPTY()),
    Field(
        "status",
        "string",
        length=20,
        default="todo",
        requires=IS_IN_SET(SUBTASK_STATUS),
    ),
    Field(
        "priority",
        "string",
        length=20,
        default="normal",
        requires=IS_IN_SET(PRIORITY_LEVELS),
    ),
    Field("start_date", "date", requires=IS_EMPTY_OR(IS_DATE())),
    Field("end_date", "date", requires=IS_EMPTY_OR(IS_DATE())),
    Field("note", "text", length=500, default=""),
    signature,
    migrate=False,
)

# Task comments / chat
db.define_table(
    "task_comment",
    Field("cid", "string", length=20, default=cid, requires=IS_NOT_EMPTY()),
    Field(
        "task_id",
        "reference tasks",
        requires=IS_IN_DB(db, "tasks.id", "%(task)s"),
        ondelete="CASCADE",
    ),
    Field(
        "user_id",
        "reference user",
        requires=IS_IN_DB(db, "user.id", "%(email)s"),
    ),
    Field("body", "text", length=2000, requires=IS_NOT_EMPTY()),
    Field(
        "visibility",
        "string",
        length=20,
        default="internal",
        requires=IS_IN_SET(COMMENT_VISIBILITY),
    ),
    Field("created_on", "datetime", default=date_fixed),
    signature,
    migrate=False,
)

# Work logs (time tracking)
db.define_table(
    "work_log",
    Field("cid", "string", length=20, default=cid, requires=IS_NOT_EMPTY()),
    Field(
        "task_id",
        "reference tasks",
        requires=IS_IN_DB(db, "tasks.id", "%(task)s"),
        ondelete="CASCADE",
    ),
    Field("work_date", "date", requires=IS_DATE()),
    Field(
        "status",
        "string",
        length=20,
        default="logged",
        requires=IS_IN_SET(WORK_LOG_STATUS),
    ),
    Field(
        "work_hours",
        "double",
        length=20,
        requires=IS_FLOAT_IN_RANGE(0, 24, None, (False, True)),
    ),
    Field("work_description", "text", length=500, requires=IS_NOT_EMPTY()),
    signature,
    migrate=False,
)

# --------------------- End Task Management Tables ---------------------

db.commit()
