from django.db import models
from django.contrib.auth.models import User

class WorkoutPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class Exercise(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    video_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class WorkoutPlanExercise(models.Model):
    workout_plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.PositiveIntegerField()
    reps = models.PositiveIntegerField()
    rest_period = models.PositiveIntegerField(help_text="in seconds")

    def __str__(self):
        return f"{self.workout_plan.name} - {self.exercise.name}"

class DailyLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    workout_plan_exercise = models.ForeignKey(WorkoutPlanExercise, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    notes = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='daily_logs/', blank=True, null=True)
    video = models.FileField(upload_to='daily_logs/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.date}"

class HealthMetric(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    body_fat_percentage = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    bmi = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    skeletal_muscle_percentage = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    muscle_mass = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    protein_percentage = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    bmr = models.PositiveIntegerField(blank=True, null=True)
    fat_free_body_weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    subcutaneous_fat_percentage = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    visceral_fat = models.PositiveIntegerField(blank=True, null=True)
    body_water_percentage = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    bone_mass = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    body_type = models.CharField(max_length=255, blank=True, null=True)
    metabolic_age = models.PositiveIntegerField(blank=True, null=True)
    blood_sugar_fasting = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.date}"
