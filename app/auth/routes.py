from flask import session, redirect, url_for

from app.auth import bp, oauth
from app.models import User
from app.auth.decorators import login_required


@bp.route("/status")
def hello():
    if email := dict(session).get("email"):
        return f"Logged in with {email}"
    return "Not logged in"


@bp.route("/protected")
@login_required
def protected(**kwargs):
    return f"Ok"


@bp.route('/login')
def login():
    google = oauth.create_client("google")
    redirect_uri = url_for('auth.authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@bp.route('/authorize')
def authorize():
    # getting auth data from google
    google = oauth.create_client("google")
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()

    # setting values to session storage
    session["email"] = user_info["email"]
    session["user_id"] = user_info["id"]

    # adding user if he is not present in users table
    if not User.find_by_id(user_info["id"]):
        User.add(User(id=user_info["id"], name=user_info["name"], email=user_info["email"]))

    return redirect('/auth/status')


@bp.route("/logout")
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect("/auth/status")
