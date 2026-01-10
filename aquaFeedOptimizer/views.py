from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

def home(request):
    return render(request, "home.html")

def signup(request):
    next_url = request.GET.get("next") or request.POST.get("next")

    if request.method == "POST":
        form = UserCreationForm(request.POST)

        for field in form.fields.values():
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (existing + " form-control").strip()

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created. You are now logged in.")
            return redirect(next_url or "aquariums:list")
    else:
        form = UserCreationForm()

        for field in form.fields.values():
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (existing + " form-control").strip()

    return render(request, "registration/signup.html", {"form": form, "next": next_url})