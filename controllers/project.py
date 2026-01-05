from py4web import action, request, abort, redirect, URL, response, Session
from py4web.utils.form import Form, FormStyleDefault
from yatl.helpers import A, TAG, XML
from pydal.validators import IS_IN_DB, IS_NOT_EMPTY

from ..common import db, session, T, auth, flash


@action("project/index")
@action.uses("project/index.html", flash,session,auth,T,db)
def index():
    rows = db(db.project).select(orderby=~db.project.id)
    return dict(rows=rows, title="Projects", add_url=URL("project/create"))


@action("project/create", method=["GET", "POST"])
@action.uses("project/form.html", flash,session,auth,T,db)
def create():
    form = Form(db.project, keep_values=True, formstyle=FormStyleDefault)
    if form.accepted:
        flash.set("Project Created")
        redirect(URL("project"))
    elif form.errors:
        flash.set("Please correct the errors", sanitize=False)
    return dict(form=form, title="Create Project", submit_label="Create")


@action("project/<project_id>/edit", method=["GET", "POST"])
@action.uses("project/form.html", flash,session,auth,T,db)
def edit(project_id=None):
    record = db.project(project_id) or abort(404)
    form = Form(
        db.project,
        record=record,
        deletable=False,
        keep_values=True,
        formstyle=FormStyleDefault,
    )
    if form.accepted:
        flash.set("Project updated")
        redirect(URL("project"))
    elif form.errors:
        flash.set("Please correct the errors", sanitize=False)
    return dict(form=form, title="Edit Project", submit_label="Update")


@action("project/<project_id>/delete", method=["POST"])
@action.uses(flash,session,auth,T,db)
def delete(project_id=None):
    record = db.project(project_id) or abort(404)
    db(db.project.id == record.id).delete()
    flash.set("Project deleted")
    redirect(URL("project"))
