from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
import google.generativeai as genai
import random
import string
from .models import WorkoutPlan


def index(request):
    return render(request, "core/index.html")


@require_http_methods(["GET", "POST"])
def generate_workout(request):

    if request.method == "POST":
        goal = request.POST.get("goal", "")
        level = request.POST.get("level", "")
        duration = request.POST.get("duration", "")

        # Random tag for unique AI response
        random_tag = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

        prompt = f"""
        (Session-ID: {random_tag})

        Create a completely unique workout plan.
        User:
        - Goal: {goal}
        - Level: {level}
        - Duration: {duration}

        Rules:
        - Output in English only.
        - Never repeat earlier workouts.
        - Vary exercise count, style, structure.
        - Add a short explanation for the plan.
        """

        # Model (Gemma)
        model = genai.GenerativeModel(
            "models/gemma-3-4b-it",
            generation_config={
                "temperature": 2.0,
                "top_p": 0.95,
                "top_k": 50,
            }
        )

        response = model.generate_content(prompt)
        ai_text = response.text  # extracted text

        # ----- SAVE TO DATABASE -----
        if request.user.is_authenticated:
            WorkoutPlan.objects.create(
                user=request.user,
                goal=goal,
                level=level,
                duration=duration,
                ai_response=ai_text   # IMPORTANT: field name matches model
            )

        context = {
            "workout_data": ai_text
        }

        return render(request, "core/generate_result.html", context)

    return render(request, "core/generate_workout.html")


def generate_result(request):
    return render(request, "core/generate_result.html")


def dashboard(request):

    if not request.user.is_authenticated:
        return redirect("login")

    plans = WorkoutPlan.objects.filter(user=request.user).order_by("-created_at")

    return render(request, "core/dashboard.html", {
        "plans": plans
    })
def view_plan(request, id):
    if not request.user.is_authenticated:
        return redirect("login")

    try:
        plan = WorkoutPlan.objects.get(id=id, user=request.user)
    except WorkoutPlan.DoesNotExist:
        return render(request, "core/view_plan.html", {
            "error": "Plan not found or access denied."
        })

    return render(request, "core/view_plan.html", {
        "plan": plan
    })