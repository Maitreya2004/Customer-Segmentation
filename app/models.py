from datetime import datetime
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

# --------- User Model ---------
class User(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    pw_hash = db.Column(db.String(255), nullable=False)
    uploads  = db.relationship("Upload", backref="uploader", lazy=True)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

# --------- Upload Model ---------
class Upload(db.Model):
    id             = db.Column(db.Integer, primary_key=True)
    user_id        = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    original_name  = db.Column(db.String(255), nullable=False)
    saved_name     = db.Column(db.String(255), nullable=False)
    clustered_name = db.Column(db.String(255))
    plot_name      = db.Column(db.String(255))
    timestamp      = db.Column(db.DateTime, default=datetime.utcnow)
