from py4web import action, request, abort, redirect, URL, response, Session
from py4web.utils.form import Form, FormStyleDefault
from yatl.helpers import A, TAG, XML
from pydal.validators import IS_EMPTY_OR, IS_IN_DB, IS_NOT_EMPTY

from ..common import db, session, T, auth, flash


def _assignee_form(record=None):
    db.task_assignee.task_id.requires = IS_IN_DB(db, "tasks.id", "%(task)s")
    db.task_assignee.user_id.requires = IS_IN_DB(db, "user.id", "%(email)s")
    form = Form(
        db.task_assignee,
        record=record,
        deletable=False,
        keep_values=True,
        formstyle=FormStyleDefault,
    )
    return form


@action("task_assignee/index")
@action.uses("task_assignee/index.html", flash,session,auth,T,db)
def index():
    rows = db(db.task_assignee).select(orderby=~db.task_assignee.id)
    return dict(rows=rows, title="Task Assignees", add_url=URL("task_assignee/create"))


@action("task_assignee/create", method=["GET", "POST"])
@action.uses("task_assignee/form.html", flash,session,auth,T,db)
def create():
    task_id = request.params.get("task_id")
    if task_id and task_id.isdigit():
        db.task_assignee.task_id.default = int(task_id)
    form = _assignee_form()
    if form.accepted:
        flash.set("Assignee added")
        redirect(URL("task_assignee"))
    elif form.errors:
        flash.set("Please correct the errors", sanitize=False)
    return dict(form=form, title="Add Assignee", submit_label="Create")


@action("task_assignee/<row_id>/edit", method=["GET", "POST"])
@action.uses("task_assignee/form.html", flash,session,auth,T,db)
def edit(row_id=None):
    record = db.task_assignee(row_id) or abort(404) 
    form = _assignee_form(record)
    if form.accepted:
        flash.set("Assignee updated")
        redirect(URL("task_assignee"))
    elif form.errors:
        flash.set("Please correct the errors", sanitize=False)
    return dict(form=form, title="Edit Assignee", submit_label="Update")


@action("task_assignee/<row_id>/delete", method=["POST"])
@action.uses(flash,session,auth,T,db)
def delete(row_id=None):
    record = db.task_assignee(row_id) or abort(404)
    db(db.task_assignee.id == record.id).delete()
    flash.set("Assignee removed")
    redirect(URL("task_assignee"))
