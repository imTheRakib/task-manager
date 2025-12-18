from py4web import action, request, abort, redirect, URL, response, Session
from py4web.utils.form import Form, FormStyleDefault
from yatl.helpers import A, TAG, XML
from pydal.validators import IS_EMPTY_OR, IS_IN_DB, IS_NOT_EMPTY

from ..common import db, session, T, auth, flash


def _subtask_form(record=None):
    db.task_subtask.parent_task_id.requires = IS_IN_DB(db, "tasks.id", "%(task)s")
    form = Form(
        db.task_subtask,
        record=record,
        deletable=False,
        keep_values=True,
        formstyle=FormStyleDefault,
    )
    return form


@action("task_subtask/index")
@action.uses("task_subtask/index.html", flash,session,auth,T,db)
def index():
    rows = db(db.task_subtask).select(orderby=~db.task_subtask.id)
    return dict(rows=rows, title="Subtasks", add_url=URL("task_subtask/create"))


@action("task_subtask/create", method=["GET", "POST"])
@action.uses("task_subtask/form.html", flash,session,auth,T,db)
def create():
    task_id = request.params.get("task_id")
    if task_id and task_id.isdigit():
        db.task_subtask.parent_task_id.default = int(task_id)
    form = _subtask_form()
    if form.accepted:
        flash.set("Subtask created")
        redirect(URL("task_subtask"))
    elif form.errors:
        flash.set("Please correct the errors", sanitize=False)
    return dict(form=form, title="Create Subtask", submit_label="Create")


@action("task_subtask/<row_id>/edit", method=["GET", "POST"])
@action.uses("task_subtask/form.html", flash,session,auth,T,db)
def edit(row_id=None):
    record = db.task_subtask(row_id) or abort(404)
    form = _subtask_form(record)
    if form.accepted:
        flash.set("Subtask updated")
        redirect(URL("task_subtask"))
    elif form.errors:
        flash.set("Please correct the errors", sanitize=False)
    return dict(form=form, title="Edit Subtask", submit_label="Update")


@action("task_subtask/<row_id>/delete", method=["POST"])
@action.uses(flash,session,auth,T,db)
def delete(row_id=None):
    record = db.task_subtask(row_id) or abort(404)
    db(db.task_subtask.id == record.id).delete()
    flash.set("Subtask deleted")
    redirect(URL("task_subtask"))
