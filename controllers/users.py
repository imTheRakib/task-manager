from py4web import action, request, abort, redirect, URL, response, Session
from py4web.utils.form import Form, FormStyleDefault
from yatl.helpers import A, TAG, XML
from pydal.validators import IS_EMPTY_OR, IS_IN_DB, IS_NOT_EMPTY

from ..common import db, session, T, auth, flash


@action("user/index")
@action.uses("user/index.html", flash,session,auth,T,db)
def index():
    rows = db(db.user).select(orderby=db.user.full_name)
    return dict(rows=rows, title="Users", add_url=URL("user/create"))


@action("user/create", method=["GET", "POST"])
@action.uses("user/form.html", flash,session,auth,T,db)
def create():
    form = Form(db.user, keep_values=True, formstyle=FormStyleDefault)
    if form.accepted:
        flash.set("User created")
        redirect(URL("user"))
    elif form.errors:
        flash.set("Please correct the errors", sanitize=False)
    return dict(form=form, title="Create User", submit_label="Create")


@action("user/<user_id>/edit", method=["GET", "POST"])
@action.uses("user/form.html", flash,session,auth,T,db)
def edit(user_id=None):
    record = db.user(user_id) or abort(404)
    form = Form(
        db.user,
        record=record,
        deletable=False,
        keep_values=True,
        formstyle=FormStyleDefault,
    )
    if form.accepted:
        flash.set("User updated")
        redirect(URL("user"))
    elif form.errors:
        flash.set("Please correct the errors", sanitize=False)
    return dict(form=form, title="Edit User", submit_label="Update")


@action("user/<user_id>/delete", method=["POST"])
@action.uses(flash,session,auth,T,db)
def delete(user_id=None):
    record = db.user(user_id) or abort(404)
    db(db.user.id == record.id).delete()
    flash.set("User deleted")
    redirect(URL("user"))
