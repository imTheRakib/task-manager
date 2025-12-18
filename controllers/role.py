from py4web import action, request, abort, redirect, URL, response, Session
from py4web.utils.form import Form, FormStyleDefault
from yatl.helpers import A, TAG, XML
from pydal.validators import IS_IN_DB, IS_NOT_EMPTY

from ..common import db, session, T, auth, flash


@action("role/index")
@action.uses("role/index.html", flash,session,auth,T,db)
def index():
    rows = db(db.role).select(orderby=db.role.name)
    return dict(rows=rows, title="Roles", add_url=URL("role/create"))


@action("role/create", method=["GET", "POST"])
@action.uses("role/form.html", flash,session,auth,T,db)
def create():
    form = Form(db.role, keep_values=True, formstyle=FormStyleDefault)
    if form.accepted:
        flash.set("Role created")
        redirect(URL("role"))
    elif form.errors:
        flash.set("Please correct the errors", sanitize=False)
    return dict(form=form, title="Create Role", submit_label="Create")


@action("role/<role_id>/edit", method=["GET", "POST"])
@action.uses("role/form.html", flash,session,auth,T,db)
def edit(role_id=None):
    record = db.role(role_id) or abort(404)
    form = Form(
        db.role,
        record=record,
        deletable=False,
        keep_values=True,
        formstyle=FormStyleDefault,
    )
    if form.accepted:
        flash.set("Role updated")
        redirect(URL("role"))
    elif form.errors:
        flash.set("Please correct the errors", sanitize=False)
    return dict(form=form, title="Edit Role", submit_label="Update")


@action("role/<role_id>/delete", method=["POST"])
@action.uses(flash,session,auth,T,db)
def delete(role_id=None):
    record = db.role(role_id) or abort(404)
    db(db.role.id == record.id).delete()
    flash.set("Role deleted")
    redirect(URL("role"))
