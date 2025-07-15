from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from user.forms import LoginForm, SignupForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from user.models import User


def signin(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        username = form.data.get("username")
        password = form.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("smart_parenting:index")
        else:
            messages.error(request, "Username/password is incorrect!")
    form = LoginForm()
    return render(request, "user/login.html", {"form": form})


def register(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = SignupForm()
    for field in form.errors:
        form[field].field.widget.attrs["class"] += " field-error"
    return render(request, "user/register.html", {"form": form})
