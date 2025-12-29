import os
from flask import Flask, render_template, request, redirect, session, url_for
from dotenv import load_dotenv
from admin.routes.brands import brands_bp
from admin.routes.cars import cars_bp
from admin.routes.managers import managers_bp
from admin.routes.requests import requests_bp
from database.models import get_pending_requests

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.secret_key = "suvtekin_secret_key"

    app.register_blueprint(brands_bp)
    app.register_blueprint(cars_bp)
    app.register_blueprint(managers_bp)
    app.register_blueprint(requests_bp)

    ADMIN_LOGIN = os.getenv("ADMIN_LOGIN")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

    @app.route("/")
    def index():
        if not session.get("logged_in"):
            return redirect("/login")
        return redirect("/dashboard")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            login = request.form["username"]
            password = request.form["password"]
            if login == ADMIN_LOGIN and password == ADMIN_PASSWORD:
                session["logged_in"] = True
                return redirect("/dashboard")
            else:
                return render_template("login.html", error="❌ Неверный логин или пароль")
        return render_template("login.html")

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect("/login")

    @app.route("/dashboard")
    def dashboard():
        if not session.get("logged_in"):
            return redirect("/login")
        pending = len(get_pending_requests())
        return render_template("dashboard.html", pending=pending)

    return app
