from py4web import action, request, abort, redirect, URL, response, Session
from py4web.utils.form import Form, FormStyleDefault
from yatl.helpers import A, TAG, XML
from pydal.validators import IS_IN_DB, IS_NOT_EMPTY

from ..common import db, session, T, auth, flash


def _module_form(record=None):
    # Limit project choices
    db.module.project_id.requires = IS_IN_DB(db, "project.id", "%(name)s")
    form = Form(
        db.module,
        record=record,
        deletable=False,
        keep_values=True,
        formstyle=FormStyleDefault,
    )
    return form


@action("module/index")
@action.uses("module/index.html", flash,session,auth,T,db)
def index():
    rows = db(db.module).select(orderby=~db.module.id)
    return dict(rows=rows, title="Modules", add_url=URL("module/create"))


@action("module/create", method=["GET", "POST"])
@action.uses("module/form.html", flash,session,auth,T,db)
def create():
    form = _module_form()
    if form.accepted:
        flash.set("Module created")
        redirect(URL("module"))
    elif form.errors:
        flash.set("Please correct the errors", sanitize=False)
    return dict(form=form, title="Create Module", submit_label="Create")


@action("module/<module_id>/edit", method=["GET", "POST"])
@action.uses("module/form.html", flash,session,auth,T,db)
def edit(module_id=None):
    record = db.module(module_id) or abort(404)
    form = _module_form(record)
    if form.accepted:
        flash.set("Module updated")
        redirect(URL("module"))
    elif form.errors:
        flash.set("Please correct the errors", sanitize=False)
    return dict(form=form, title="Edit Module", submit_label="Update")


@action("module/<module_id>/delete", method=["POST"])
@action.uses(flash,session,auth,T,db)
def delete(module_id=None):
    record = db.module(module_id) or abort(404)
    db(db.module.id == record.id).delete()
    flash.set("Module deleted")
    redirect(URL("module"))
