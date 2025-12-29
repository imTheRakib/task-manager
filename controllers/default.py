from py4web import action, request, abort, redirect, URL, response, Session
from py4web.utils.form import Form, FormStyleDefault
from yatl.helpers import A
from ..common import db, session, T, auth, flash
import json

@action("index")
@action.uses("index.html", session, flash,db)
def index():
    # return dict(redirect(URL('login', 'index')))
    return dict(redirect(URL('dashboard', 'index')))