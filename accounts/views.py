from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# ------------------------ SIGNUP ------------------------
def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            return render(request, "accounts/signup.html", {
                "error": "User already exists."
            })

        # Create user
        user = User.objects.create_user(username=username, password=password)

        # Auto-login after signup
        login(request, user)

        return redirect("dashboard")

    return render(request, "accounts/signup.html")


# ------------------------ LOGIN ------------------------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")

        return render(request, "accounts/login.html", {
            "error": "Invalid username or password"
        })

    return render(request, "accounts/login.html")


# ------------------------ LOGOUT ------------------------
def logout_view(request):
    logout(request)
    return redirect("login")