from flask import Blueprint, render_template, request, redirect, session
from database.models import get_all_cars, get_all_brands, add_car, delete_car

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
    add_car(brand_id, model, year, transmission, fuel, price)
    return redirect("/cars")

@cars_bp.route("/delete/<int:car_id>")
def delete_car_route(car_id):
    if not session.get("logged_in"):
        return redirect("/login")
    delete_car(car_id)
    return redirect("/cars")
