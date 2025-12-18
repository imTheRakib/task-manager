from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from ..common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash


@action("dashboard/index")
@action.uses("dashboard/index.html",session,flash,db)
def index():
    """Simple dashboard summary counts."""
    projects = db(db.project).count()
    modules = db(db.module).count()
    tasks_total = db(db.tasks).count()
    tasks_open = db(db.tasks.task_status.belongs(["todo", "in_progress", "blocked", "in_review"])).count()
    tasks_done = db(db.tasks.task_status == "done").count()
    users = db(db.user).count()
    return dict(
        projects=projects,
        modules=modules,
        tasks_total=tasks_total,
        tasks_open=tasks_open,
        tasks_done=tasks_done,
        users=users,
    )
