from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("generate-workout/", views.generate_workout, name="generate_workout"),
    path("generate-result/", views.generate_result, name="generate_result"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("plan/<int:id>/", views.view_plan, name="view_plan")
]