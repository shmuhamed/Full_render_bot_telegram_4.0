import os
from flask import Blueprint, render_template, request, redirect, session, current_app
from werkzeug.utils import secure_filename
from database.models import get_all_cars, get_all_brands, add_car, delete_car

cars_bp = Blueprint("cars", __name__, url_prefix="/cars")

UPLOAD_FOLDER = "admin/static/uploads"

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

    image_path = None
    file = request.files.get("image")
    if file and file.filename:
        filename = secure_filename(file.filename)
        upload_dir = os.path.join(current_app.root_path, "static", "uploads")
        os.makedirs(upload_dir, exist_ok=True)
        file.save(os.path.join(upload_dir, filename))
        image_path = f"/static/uploads/{filename}"

    # добавляем с фото
    from database.models import get_session, Car
    session = get_session()
    new_car = Car(brand_id=brand_id, model=model, year=year,
                  transmission=transmission, fuel=fuel, price=price,
                  image=image_path)
    session.add(new_car)
    session.commit()

    return redirect("/cars")

@cars_bp.route("/delete/<int:car_id>")
def delete_car_route(car_id):
    if not session.get("logged_in"):
        return redirect("/login")
    delete_car(car_id)
    return redirect("/cars")
