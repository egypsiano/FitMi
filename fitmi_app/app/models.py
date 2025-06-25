from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(256)) # Increased length for future hash algorithm changes
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships (examples, will be expanded later)
    # workout_logs = db.relationship('WorkoutLog', backref='author', lazy='dynamic')
    # meal_logs = db.relationship('MealLog', backref='author', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Future models can be added here, e.g.:
# class Workout(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     type = db.Column(db.String(50)) # E.g., 'Home', 'Gym'
#     description = db.Column(db.Text)
#     muscle_group = db.Column(db.String(100))
#     video_url = db.Column(db.String(200))
#     image_url = db.Column(db.String(200))
#     warm_up = db.Column(db.Text)
#     cool_down = db.Column(db.Text)
#     created_by_user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # If users can add workouts

# class Nutrition(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     meal_name = db.Column(db.String(100), nullable=False)
#     calories = db.Column(db.Integer)
#     protein = db.Column(db.Float)
#     carbs = db.Column(db.Float)
#     fats = db.Column(db.Float)
#     recipe = db.Column(db.Text)
#     source_url = db.Column(db.String(200)) # E.g., from MyFitnessPal or other sites
#     created_by_user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # If users can add meals

# class UserProfile(db.Model): # For dashboard items
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
#     weight_kg = db.Column(db.Float)
#     height_cm = db.Column(db.Float)
#     # BMR, BMI, Fat percentage could be calculated fields or stored if historical tracking is needed
#     user = db.relationship("User", backref=db.backref("profile", uselist=False))
