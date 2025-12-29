import os
from flask import Blueprint, render_template, request, redirect, session, current_app
from werkzeug.utils import secure_filename
from PIL import Image
from database.models import get_all_cars, get_all_brands, add_car_with_images, get_session, Car, CarImage

cars_bp = Blueprint("cars", __name__, url_prefix="/cars")

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
MAX_WIDTH = 1280

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def compress_image(input_path, output_path):
    try:
        img = Image.open(input_path)
        img.thumbnail((MAX_WIDTH, MAX_WIDTH))
        img.convert("RGB").save(output_path, "JPEG", optimize=True, quality=80)
    except Exception as e:
        print(f"⚠️ Ошибка сжатия изображения: {e}")

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
    is_featured = "is_featured" in request.form  # ✅ Новое поле

    upload_dir = os.path.join(current_app.root_path, "static", "uploads")
    os.makedirs(upload_dir, exist_ok=True)

    image_paths = []
    files = request.files.getlist("images")

    for file in files[:5]:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            original_path = os.path.join(upload_dir, filename)
            compressed_path = os.path.join(upload_dir, f"compressed_{filename}")

            file.save(original_path)
            compress_image(original_path, compressed_path)
            os.remove(original_path)
            image_paths.append(f"/static/uploads/{os.path.basename(compressed_path)}")

    add_car_with_images(brand_id, model, year, transmission, fuel, price, image_paths, is_featured)
    return redirect("/cars")

@cars_bp.route("/delete/<int:car_id>")
def delete_car_route(car_id):
    if not session.get("logged_in"):
        return redirect("/login")

    session_db = get_session()
    car = session_db.get(Car, car_id)
    if car:
        for img in car.images:
            image_path = os.path.join(current_app.root_path, img.path.lstrip("/"))
            if os.path.exists(image_path):
                try:
                    os.remove(image_path)
                except Exception as e:
                    print(f"⚠️ Ошибка удаления {image_path}: {e}")
        session_db.delete(car)
        session_db.commit()
    return redirect("/cars")
