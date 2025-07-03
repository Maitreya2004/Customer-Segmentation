from flask import Blueprint, render_template, request, redirect, url_for, session, current_app as app, flash, send_from_directory
from pathlib import Path
from functools import wraps
from .models import Upload, db
from .utils import allowed, cluster_csv

main_bp = Blueprint("main", __name__)

# ---------- Login guard ----------
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "uid" not in session:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return wrapper

# ---------- Dashboard ----------
@main_bp.route("/")
@login_required
def dashboard():
    uploads = (
        Upload.query
        .filter_by(user_id=session["uid"])
        .order_by(Upload.timestamp.desc())
        .all()
    )
    return render_template("dashboard.html", uploads=uploads)

# ---------- CSV Upload ----------
@main_bp.route("/upload", methods=["POST"])
@login_required
def upload():
    file = request.files.get("file")
    if not file or not allowed(file.filename):
        flash("Please upload a CSV file.", "warning")
        return redirect(url_for("main.dashboard"))

    saved_path = Path(app.config["UPLOAD_FOLDER"]) / file.filename
    file.save(saved_path)

    try:
        clustered_path, plot_path, preview_html = cluster_csv(saved_path)
    except Exception as e:
        flash(str(e), "danger")
        return redirect(url_for("main.dashboard"))

    rec = Upload(
        user_id=session["uid"],
        original_name=file.filename,
        saved_name=saved_path.name,
        clustered_name=Path(clustered_path).name,
        plot_name=Path(plot_path).name if plot_path else None,
    )
    db.session.add(rec)
    db.session.commit()

    return render_template(
        "result.html",
        table=preview_html,
        plot=(url_for("static", filename=f"uploads/{rec.plot_name}") if rec.plot_name else None),
        download=url_for("main.download_file", fname=rec.clustered_name),
    )

# ---------- Download clustered CSV ----------
@main_bp.route("/download/<path:fname>")
@login_required
def download_file(fname):
    return send_from_directory(Path(app.config["UPLOAD_FOLDER"]), fname, as_attachment=True)
