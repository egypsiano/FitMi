from django.urls import path
from . import views

urlpatterns = [
    path('workout-plan/', views.workout_plan, name='workout_plan'),
    path('daily-log/', views.daily_log, name='daily_log'),
    path('health-metrics/', views.health_metrics, name='health_metrics'),
]
