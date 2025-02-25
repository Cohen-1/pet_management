import os
from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"

# Configure both PostgreSQL and MySQL connections
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:password@localhost:5432/pet_db"
app.config["SQLALCHEMY_BINDS"] = {
    "mysql_db": "mysql+pymysql://root:password@localhost/mysql_pet_db"
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Base class
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Pet Table in PostgreSQL
class Pet(db.Model, Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    species: Mapped[str] = mapped_column(String(50), nullable=False)
    weight: Mapped[float] = mapped_column(Float, nullable=False)

# Pet Table in MySQL
class PetMySQL(db.Model, Base):
    __bind_key__ = "mysql_db"  # Specify the MySQL database
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    species: Mapped[str] = mapped_column(String(50), nullable=False)
    weight: Mapped[float] = mapped_column(Float, nullable=False)

# Initialize DB
with app.app_context():
    db.create_all()
    db.create_all(bind="mysql_db")  # Create tables in MySQL

# Home route
@app.route("/")
def home():
    pets_pg = Pet.query.all()
    pets_mysql = PetMySQL.query.all()
    return render_template("index.html", pets_pg=pets_pg, pets_mysql=pets_mysql)

# Add pet to PostgreSQL
@app.route("/add_pg", methods=["POST"])
def add_pet_pg():
    new_pet = Pet(
        name=request.form["name"],
        age=int(request.form["age"]),
        species=request.form["species"],
        weight=float(request.form["weight"]),
    )
    db.session.add(new_pet)
    db.session.commit()
    flash("Pet added to PostgreSQL!", "success")
    return redirect("/")

# Add pet to MySQL
@app.route("/add_mysql", methods=["POST"])
def add_pet_mysql():
    new_pet = PetMySQL(
        name=request.form["name"],
        age=int(request.form["age"]),
        species=request.form["species"],
        weight=float(request.form["weight"]),
    )
    db.session.add(new_pet)
    db.session.commit()
    flash("Pet added to MySQL!", "success")
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
