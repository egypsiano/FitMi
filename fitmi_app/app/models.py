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


# Association table for WorkoutRoutine and Exercise (Many-to-Many)
routine_exercises = db.Table('routine_exercises',
    db.Column('exercise_id', db.Integer, db.ForeignKey('exercise.id'), primary_key=True),
    db.Column('routine_id', db.Integer, db.ForeignKey('workout_routine.id'), primary_key=True),
    db.Column('sets', db.Integer),
    db.Column('reps', db.String(50)), # e.g., "8-12" or "AMRAP"
    db.Column('duration_seconds', db.Integer, nullable=True), # For timed exercises
    db.Column('rest_time_seconds', db.Integer, nullable=True),
    db.Column('order', db.Integer) # To define exercise sequence in a routine
)

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    body_part = db.Column(db.String(100), index=True) # E.g., "Chest", "Legs", "Full Body"
    equipment_needed = db.Column(db.String(150), default="None")
    difficulty = db.Column(db.String(50), index=True) # E.g., "Beginner", "Intermediate", "Advanced"
    instructions = db.Column(db.Text, nullable=True)
    video_url = db.Column(db.String(255), nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    source_url = db.Column(db.String(255), nullable=True) # E.g., from MuscleWiki
    # Routines that include this exercise are accessed via the backref from WorkoutRoutine.exercises

    def __repr__(self):
        return f'<Exercise {self.name}>'

class WorkoutRoutine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    type = db.Column(db.String(50), index=True) # E.g., "Home", "Gym", "Cardio", "Kegel"
    general_warm_up = db.Column(db.Text, nullable=True)
    general_cool_down = db.Column(db.Text, nullable=True)
    created_by_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True) # Nullable for admin/system created
    is_public = db.Column(db.Boolean, default=True, index=True) # Default to public for admin, users can choose
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    creator = db.relationship('User', backref=db.backref('created_routines', lazy='dynamic'))
    exercises = db.relationship('Exercise', secondary=routine_exercises,
                                backref=db.backref('routines', lazy='dynamic'),
                                lazy='dynamic')

    def __repr__(self):
        return f'<WorkoutRoutine {self.name}>'

# Association table for Meal and FoodItem (Many-to-Many)
meal_food_items = db.Table('meal_food_items',
    db.Column('meal_id', db.Integer, db.ForeignKey('meal.id'), primary_key=True),
    db.Column('food_item_id', db.Integer, db.ForeignKey('food_item.id'), primary_key=True),
    db.Column('quantity_grams', db.Float, nullable=False) # Amount of this food item in this meal
)

class FoodItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, index=True)
    # Nutritional info per 100g
    calories_per_100g = db.Column(db.Float, nullable=True)
    protein_per_100g = db.Column(db.Float, nullable=True)
    carbs_per_100g = db.Column(db.Float, nullable=True)
    fat_per_100g = db.Column(db.Float, nullable=True)
    serving_size_grams = db.Column(db.Float, nullable=True, comment="Optional default serving size in grams")
    source_url = db.Column(db.String(255), nullable=True) # E.g., from MyFitnessPal or other nutrition sites
    # Meals that include this food item are accessed via the backref from Meal.food_items

    def __repr__(self):
        return f'<FoodItem {self.name}>'

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    created_by_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True) # Nullable for admin/system created
    is_public = db.Column(db.Boolean, default=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    creator = db.relationship('User', backref=db.backref('created_meals', lazy='dynamic'))
    food_items = db.relationship('FoodItem', secondary=meal_food_items,
                                 backref=db.backref('meals', lazy='dynamic'),
                                 lazy='dynamic')

    def __repr__(self):
        return f'<Meal {self.name}>'

class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    weight_kg = db.Column(db.Float, nullable=True)
    height_cm = db.Column(db.Float, nullable=True)
    birth_date = db.Column(db.Date, nullable=True)
    gender = db.Column(db.String(20), nullable=True) # E.g., "male", "female", "other", "prefer_not_to_say"
    activity_level = db.Column(db.String(50), nullable=True, comment="E.g., sedentary, light, moderate, active, very_active")
    # BMR, BMI, Fat percentage will be calculated dynamically or can be stored if history is needed.
    # For now, we store the inputs for these calculations.

    user = db.relationship('User', backref=db.backref('profile', uselist=False, lazy='joined')) # uselist=False for one-to-one

    def __repr__(self):
        return f'<UserProfile for {self.user.username if self.user else "N/A"}>'
