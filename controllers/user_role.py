from py4web import action, request, abort, redirect, URL, response, Session
from py4web.utils.form import Form, FormStyleDefault
from yatl.helpers import A, TAG, XML
from pydal.validators import IS_EMPTY_OR, IS_IN_DB, IS_NOT_EMPTY

from ..common import db, session, T, auth, flash


def _user_role_form(record=None):
    db.user_role.user_id.requires = IS_IN_DB(db, "user.id", "%(email)s")
    db.user_role.role_id.requires = IS_IN_DB(db, "role.id", "%(name)s")
    form = Form(
        db.user_role,
        record=record,
        deletable=False,
        keep_values=True,
        formstyle=FormStyleDefault,
    )
    return form


@action("user_role/index")
@action.uses(db, session, T, auth.user, "user_role/index.html")
def index():
    rows = db(db.user_role).select(orderby=~db.user_role.id)
    return dict(rows=rows, title="User Roles", add_url=URL("user_role/create"))


@action("user_role/create", method=["GET", "POST"])
@action.uses("user_role/form.html", flash,session,auth,T,db)
def create():
    form = _user_role_form()
    if form.accepted:
        flash.set("User role assigned")
        redirect(URL("user_role"))
    elif form.errors:
        flash.set("Please correct the errors", sanitize=False)
    return dict(form=form, title="Assign Role", submit_label="Create")


@action("user_role/<row_id>/edit", method=["GET", "POST"])
@action.uses("user_role/form.html", flash,session,auth,T,db)
def edit(row_id=None):
    record = db.user_role(row_id) or abort(404)
    form = _user_role_form(record)
    if form.accepted:
        flash.set("User role updated")
        redirect(URL("user_role"))
    elif form.errors:
        flash.set("Please correct the errors", sanitize=False)
    return dict(form=form, title="Edit User Role", submit_label="Update")


@action("user_role/<row_id>/delete", method=["POST"])
@action.uses(flash,session,auth,T,db)
def delete(row_id=None):
    record = db.user_role(row_id) or abort(404)
    db(db.user_role.id == record.id).delete()
    flash.set("User role removed")
    redirect(URL("user_role"))
