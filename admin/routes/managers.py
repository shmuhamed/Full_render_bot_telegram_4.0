from flask import Blueprint, render_template, request, redirect, session
from database.models import get_all_managers, add_manager, delete_manager

managers_bp = Blueprint("managers", __name__, url_prefix="/managers")

@managers_bp.route("/")
def show_managers():
    if not session.get("logged_in"):
        return redirect("/login")
    managers = get_all_managers()
    return render_template("managers.html", managers=managers)

@managers_bp.route("/add", methods=["POST"])
def add_new_manager():
    if not session.get("logged_in"):
        return redirect("/login")
    name = request.form["name"]
    surname = request.form["surname"]
    phone = request.form["phone"]
    email = request.form["email"]
    telegram = request.form["telegram"]
    add_manager(name, surname, phone, email, telegram)
    return redirect("/managers")

@managers_bp.route("/delete/<int:manager_id>")
def delete_manager_route(manager_id):
    if not session.get("logged_in"):
        return redirect("/login")
    delete_manager(manager_id)
    return redirect("/managers")
