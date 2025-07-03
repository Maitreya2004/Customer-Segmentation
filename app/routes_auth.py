from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .models import User, db

auth_bp = Blueprint("auth", __name__)

# ---------- Register ----------
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        pw = request.form["password"]

        if User.query.filter_by(username=username).first():
            flash("Username already exists", "danger")
            return redirect(url_for("auth.register"))

        user = User(username=username)
        user.set_password(pw)

        db.session.add(user)
        db.session.commit()

        flash("Account created. Please sign in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")

# ---------- Login ----------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()

        if user and user.check_password(request.form["password"]):
            session["uid"] = user.id
            return redirect(url_for("main.dashboard"))

        flash("Invalid credentials", "danger")

    return render_template("login.html")

# ---------- Logout ----------
@auth_bp.route("/logout")
def logout():
    session.pop("uid", None)
    return redirect(url_for("auth.login"))
