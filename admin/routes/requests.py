from flask import Blueprint, render_template, redirect, session
from database.models import get_all_requests, mark_request_done

requests_bp = Blueprint("requests", __name__, url_prefix="/requests")

@requests_bp.route("/")
def show_requests():
    if not session.get("logged_in"):
        return redirect("/login")
    requests = get_all_requests()
    return render_template("requests.html", requests=requests)

@requests_bp.route("/done/<int:req_id>")
def mark_done(req_id):
    if not session.get("logged_in"):
        return redirect("/login")
    mark_request_done(req_id)
    return redirect("/requests")
