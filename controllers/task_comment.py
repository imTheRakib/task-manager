from py4web import action, request, abort, redirect, URL, response, Session
from py4web.utils.form import Form, FormStyleDefault
from yatl.helpers import A, TAG, XML
from pydal.validators import IS_EMPTY_OR, IS_IN_DB, IS_NOT_EMPTY

from ..common import db, session, T, auth, flash


def _comment_form(record=None):
    db.task_comment.task_id.requires = IS_IN_DB(db, "tasks.id", "%(task)s")
    db.task_comment.user_id.requires = IS_IN_DB(db, "user.id", "%(email)s")
    form = Form(
        db.task_comment,
        record=record,
        deletable=False,
        keep_values=True,
        formstyle=FormStyleDefault,
    )
    return form


@action("task_comment/index")
@action.uses("task_comment/index.html", flash,session,auth,T,db)
def index():
    task_id = request.params.get("task_id")
    query = db.task_comment.id > 0
    if task_id:
        query &= db.task_comment.task_id == task_id
    rows = db(query).select(orderby=~db.task_comment.id)
    return dict(rows=rows, title="Comments", add_url=URL("task_comment/create"))


@action("task_comment/create", method=["GET", "POST"])
@action.uses("task_comment/form.html", flash,session,auth,T,db)
def create():
    task_id = request.params.get("task_id")
    if task_id and task_id.isdigit():
        db.task_comment.task_id.default = int(task_id)
    form = _comment_form()
    if form.accepted:
        flash.set("Comment added")
        redirect(URL("task_comment"))
    elif form.errors:
        flash.set("Please correct the errors", sanitize=False)
    return dict(form=form, title="Add Comment", submit_label="Create")


@action("task_comment/<row_id>/edit", method=["GET", "POST"])
@action.uses("task_comment/form.html", flash,session,auth,T,db)
def edit(row_id=None):
    record = db.task_comment(row_id) or abort(404)
    form = _comment_form(record)
    if form.accepted:
        flash.set("Comment updated")
        redirect(URL("task_comment"))
    elif form.errors:
        flash.set("Please correct the errors", sanitize=False)
    return dict(form=form, title="Edit Comment", submit_label="Update")


@action("task_comment/<row_id>/delete", method=["POST"])
@action.uses(flash,session,auth,T,db)
def delete(row_id=None):
    record = db.task_comment(row_id) or abort(404)
    db(db.task_comment.id == record.id).delete()
    flash.set("Comment deleted")
    redirect(URL("task_comment"))
