from py4web import action, request, abort, redirect, URL, response, Session
from py4web.utils.form import Form, FormStyleDefault
from yatl.helpers import A, TAG, XML
from pydal.validators import IS_EMPTY_OR, IS_IN_DB, IS_NOT_EMPTY

from ..common import db, session, T, auth, flash


def _task_form(record=None):
    db.tasks.project_id.requires = IS_IN_DB(db, "project.id", "%(name)s")
    db.tasks.module_id.requires = IS_EMPTY_OR(IS_IN_DB(db, "module.id", "%(name)s"))
    db.tasks.owner_id.requires = IS_IN_DB(db, "user.id", "%(email)s")
    db.tasks.reliever_id.requires = IS_EMPTY_OR(IS_IN_DB(db, "user.id", "%(email)s"))
    form = Form(
        db.tasks,
        record=record,
        deletable=False,
        keep_values=True,
        formstyle=FormStyleDefault,
    )
    return form


@action("tasks/index")
@action.uses("tasks/index.html", flash,session,auth,T,db)
def index():
    status = request.params.get("status")
    query = db.tasks.id > 0
    if status:
        query &= db.tasks.task_status == status
    rows = db(query).select(orderby=~db.tasks.id)
    status_options = db.tasks.task_status.requires.options()
    return dict(rows=rows, title="Tasks", add_url=URL("tasks/create"), status_filter=status or "", status_options=status_options)


@action("tasks/create", method=["GET", "POST"])
@action.uses("tasks/form.html", flash,session,auth,T,db)
def create():
    form = _task_form()
    if form.accepted:
        flash.set("Task created")
        redirect(URL("tasks"))
    elif form.errors:
        flash.set("Please correct the errors", sanitize=False)
    return dict(form=form, title="Create Task", submit_label="Create")


@action("tasks/<task_id>/edit", method=["GET", "POST"])
@action.uses("tasks/form.html", flash,session,auth,T,db)
def edit(task_id=None):
    record = db.tasks(task_id) or abort(404)
    form = _task_form(record)
    if form.accepted:
        flash.set("Task updated")
        redirect(URL("tasks"))
    elif form.errors:
        flash.set("Please correct the errors", sanitize=False)
    return dict(form=form, title="Edit Task", submit_label="Update")


@action("tasks/<task_id>")
@action.uses("tasks/detail.html", flash,session,auth,T,db)
def detail(task_id=None):
    record = db.tasks(task_id) or abort(404)
    logs = db(db.tasks_log.task_id == record.id).select(orderby=~db.tasks_log.changed_on)
    subtasks = db(db.task_subtask.parent_task_id == record.id).select(orderby=~db.task_subtask.id)
    comments = db(db.task_comment.task_id == record.id).select(orderby=~db.task_comment.id)
    assignees = db(db.task_assignee.task_id == record.id).select(orderby=db.task_assignee.id)
    status_options = db.tasks.task_status.requires.options()
    return dict(task=record, logs=logs, subtasks=subtasks, comments=comments, assignees=assignees, status_options=status_options, title="Task Details")


@action("tasks/<task_id>/status", method=["POST"])
@action.uses(flash,session,auth,T,db)
def update_status(task_id=None):
    record = db.tasks(task_id) or abort(404)
    new_status = request.forms.get("status")
    valid_statuses = [opt[0] for opt in db.tasks.task_status.requires.options()]
    if new_status not in valid_statuses:
        abort(400)
    old_status = record.task_status
    if old_status != new_status:
        db.tasks_log.insert(
            task_id=record.id,
            from_status=old_status,
            to_status=new_status,
            changed_by=auth.current_user.get("id"),
            note=request.forms.get("note", ""),
        )
        record.update_record(task_status=new_status)
    redirect(URL("tasks/%s" % record.id))


@action("tasks/<task_id>/delete", method=["POST"])
@action.uses(flash,session,auth,T,db)
def delete(task_id=None):
    record = db.tasks(task_id) or abort(404)
    db(db.tasks.id == record.id).delete()
    flash.set("Task deleted")
    redirect(URL("tasks"))
