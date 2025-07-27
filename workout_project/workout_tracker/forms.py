from django import forms
from .models import DailyLog, HealthMetric

class DailyLogForm(forms.ModelForm):
    class Meta:
        model = DailyLog
        fields = ['date', 'workout_plan_exercise', 'weight', 'notes', 'image', 'video']

class HealthMetricForm(forms.ModelForm):
    class Meta:
        model = HealthMetric
        fields = [
            'date', 'weight', 'body_fat_percentage', 'bmi',
            'skeletal_muscle_percentage', 'muscle_mass', 'protein_percentage',
            'bmr', 'fat_free_body_weight', 'subcutaneous_fat_percentage',
            'visceral_fat', 'body_water_percentage', 'bone_mass', 'body_type',
            'metabolic_age', 'blood_sugar_fasting'
        ]
