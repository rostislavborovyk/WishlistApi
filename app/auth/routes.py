from flask import session, redirect, url_for

from app.auth import bp, oauth


@bp.route("/")
def hello():
    email = dict(session).get("email")
    id_ = dict(session).get("id")
    return f"Of, {email}, {id_}"


@bp.route('/login')
def login():
    google = oauth.create_client("google")
    redirect_uri = url_for('auth.authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@bp.route('/authorize')
def authorize():
    google = oauth.create_client("google")
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()
    session["email"] = user_info["email"]
    session["id"] = user_info["id"]
    return redirect('/auth')


@bp.route("/logout")
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect("/auth")
