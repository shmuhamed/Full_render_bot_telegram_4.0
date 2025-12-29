from flask import Blueprint, render_template, request, redirect, session
from database.models import get_all_brands, add_brand, delete_brand

brands_bp = Blueprint("brands", __name__, url_prefix="/brands")

@brands_bp.route("/")
def show_brands():
    if not session.get("logged_in"):
        return redirect("/login")
    brands = get_all_brands()
    return render_template("brands.html", brands=brands)

@brands_bp.route("/add", methods=["POST"])
def add_new_brand():
    if not session.get("logged_in"):
        return redirect("/login")
    name = request.form["name"]
    add_brand(name)
    return redirect("/brands")

@brands_bp.route("/delete/<int:brand_id>")
def delete_brand_route(brand_id):
    if not session.get("logged_in"):
        return redirect("/login")
    delete_brand(brand_id)
    return redirect("/brands")
