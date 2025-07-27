from django.shortcuts import render, redirect
from .models import WorkoutPlan, WorkoutPlanExercise, Exercise, DailyLog, HealthMetric
from .forms import DailyLogForm, HealthMetricForm

def workout_plan(request):
    # Dummy data for now
    exercise1 = Exercise(name="Bench Press", description="Lay on a bench and press a barbell up and down.")
    exercise2 = Exercise(name="Squat", description="Stand with a barbell on your shoulders and squat down.")

    workout_plan = WorkoutPlan(name="My Workout Plan", description="A plan to get big and strong.")

    plan_exercise1 = WorkoutPlanExercise(workout_plan=workout_plan, exercise=exercise1, sets=3, reps=10, rest_period=60)
    plan_exercise2 = WorkoutPlanExercise(workout_plan=workout_plan, exercise=exercise2, sets=3, reps=12, rest_period=90)

    plan_exercises = [plan_exercise1, plan_exercise2]

    context = {
        'workout_plan': workout_plan,
        'plan_exercises': plan_exercises,
    }
    return render(request, 'workout_tracker/workout_plan.html', context)

def daily_log(request):
    if request.method == 'POST':
        form = DailyLogForm(request.POST, request.FILES)
        if form.is_valid():
            daily_log = form.save(commit=False)
            daily_log.user = request.user
            daily_log.save()
            return redirect('daily_log')
    else:
        form = DailyLogForm()

    daily_logs = DailyLog.objects.filter(user=request.user).order_by('-date')

    context = {
        'form': form,
        'daily_logs': daily_logs,
    }
    return render(request, 'workout_tracker/daily_log.html', context)

import datetime

def health_metrics(request):
    if request.method == 'POST':
        form = HealthMetricForm(request.POST)
        if form.is_valid():
            health_metric = form.save(commit=False)
            health_metric.user = request.user
            health_metric.save()
            return redirect('health_metrics')
    else:
        form = HealthMetricForm()

    health_metrics = HealthMetric.objects.filter(user=request.user).order_by('date')

    # AI-Generated Weekly Updates
    weekly_update = ""
    if health_metrics.count() > 1:
        today = datetime.date.today()
        last_week = today - datetime.timedelta(days=7)

        recent_metrics = health_metrics.filter(date__gte=last_week)

        if recent_metrics.count() > 1:
            latest_metric = recent_metrics.latest('date')
            previous_metric = recent_metrics.exclude(pk=latest_metric.pk).latest('date')

            if latest_metric.weight and previous_metric.weight:
                if latest_metric.weight < previous_metric.weight:
                    weekly_update += "Great job on losing weight this week! "
                else:
                    weekly_update += "Your weight has increased this week. Let's work on that! "

            if latest_metric.body_fat_percentage and previous_metric.body_fat_percentage:
                if latest_metric.body_fat_percentage < previous_metric.body_fat_percentage:
                    weekly_update += "You've also reduced your body fat percentage. Keep it up!"
                else:
                    weekly_update += "Your body fat percentage has increased. Let's focus on your diet and cardio."

    context = {
        'form': form,
        'health_metrics': health_metrics,
        'weekly_update': weekly_update,
    }
    return render(request, 'workout_tracker/health_metrics.html', context)
