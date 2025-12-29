import os
from flask import Blueprint, render_template, request, redirect, session, current_app
from werkzeug.utils import secure_filename
from database.models import get_all_cars, get_all_brands, add_car_with_images, delete_car

cars_bp = Blueprint("cars", __name__, url_prefix="/cars")

@cars_bp.route("/")
def show_cars():
    if not session.get("logged_in"):
        return redirect("/login")
    cars = get_all_cars()
    brands = get_all_brands()
    return render_template("cars.html", cars=cars, brands=brands)

@cars_bp.route("/add", methods=["POST"])
def add_new_car():
    if not session.get("logged_in"):
        return redirect("/login")

    brand_id = request.form["brand"]
    model = request.form["model"]
    year = request.form["year"]
    price = request.form["price"]
    transmission = request.form["transmission"]
    fuel = request.form["fuel"]

    upload_dir = os.path.join(current_app.root_path, "static", "uploads")
    os.makedirs(upload_dir, exist_ok=True)

    image_paths = []
    files = request.files.getlist("images")
    for file in files[:5]:  # максимум 5 фото
        if file and file.filename:
            filename = secure_filename(file.filename)
            file.save(os.path.join(upload_dir, filename))
            image_paths.append(f"/static/uploads/{filename}")

    add_car_with_images(brand_id, model, year, transmission, fuel, price, image_paths)
    return redirect("/cars")

@cars_bp.route("/delete/<int:car_id>")
def delete_car_route(car_id):
    if not session.get("logged_in"):
        return redirect("/login")
    delete_car(car_id)
    return redirect("/cars")
