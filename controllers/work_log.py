from py4web import action, request, abort, redirect, URL, response, Session
from py4web.utils.form import Form, FormStyleDefault
from yatl.helpers import A, TAG, XML
from pydal.validators import IS_EMPTY_OR, IS_IN_DB, IS_NOT_EMPTY

from ..common import db, session, T, auth, flash


def _work_log_form(record=None):
    db.work_log.task_id.requires = IS_IN_DB(db, "tasks.id", "%(task)s")
    form = Form(
        db.work_log,
        record=record,
        deletable=False,
        keep_values=True,
        formstyle=FormStyleDefault,
    )
    return form


@action("work_log/index")
@action.uses("work_log/index.html", flash,session,auth,T,db)
def index():
    rows = db(db.work_log).select(orderby=~db.work_log.id)
    return dict(rows=rows, title="Work Logs", add_url=URL("work_log/create"))


@action("work_log/create", method=["GET", "POST"])
@action.uses("work_log/form.html", flash,session,auth,T,db)
def create():
    form = _work_log_form()
    if form.accepted:
        flash.set("Work log created")
        redirect(URL("work_log"))
    elif form.errors:
        flash.set("Please correct the errors", sanitize=False)
    return dict(form=form, title="Create Work Log", submit_label="Create")


@action("work_log/<log_id>/edit", method=["GET", "POST"])
@action.uses("work_log/form.html", flash,session,auth,T,db)
def edit(log_id=None):
    record = db.work_log(log_id) or abort(404)
    form = _work_log_form(record)
    if form.accepted:
        flash.set("Work log updated")
        redirect(URL("work_log"))
    elif form.errors:
        flash.set("Please correct the errors", sanitize=False)
    return dict(form=form, title="Edit Work Log", submit_label="Update")


@action("work_log/<log_id>/delete", method=["POST"])
@action.uses(flash,session,auth,T,db)
def delete(log_id=None):
    record = db.work_log(log_id) or abort(404)
    db(db.work_log.id == record.id).delete()
    flash.set("Work log deleted")
    redirect(URL("work_log"))
