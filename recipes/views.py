from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required(login_url="/login/")
def recipes_page(request):
    if request.method == "POST":
        data = request.POST
        recipe_name = data.get("recipe_name")
        recipe_desc = data.get("recipe_desc")
        recipe_image = request.FILES.get("recipe_image")
        Recipes.objects.create(
            recipe_name=recipe_name,
            recipe_desc=recipe_desc,
            recipe_image=recipe_image)
        return redirect('/')
    querySet = Recipes.objects.all()
    query = request.GET.get("search")
    if query:
        querySet = querySet.filter(recipe_name__icontains = query)
    context = {"title": "Home", "recipes": querySet}
    return render(request, "recipes_page.html", context)


@login_required(login_url="/login/")
def update_recipe(request, id):
    recipe = Recipes.objects.get(id=id)
    if request.method=="POST":
        recipe.recipe_name = request.POST.get("recipe_name")
        recipe.recipe_desc = request.POST.get("recipe_desc")
        if request.FILES.get("recipe_image"):
            recipe.recipe_image = request.FILES.get("recipe_image")
        recipe.save()
        return redirect('/')
    context = {"title": "Update Recipe", "recipe": recipe}
    return render(request, "update_recipe.html", context)


@login_required(login_url="/login/")
def delete_recipe(request, id):
    Recipes.objects.get(id=id).delete()
    return redirect('/')


def login_page(request):
    if request.method == "POST":
        user_name = request.POST.get("user_name")
        password = request.POST.get("password")
        user = User.objects.filter(username=user_name)
        if not user.exists():
            messages.error(request, "User does not exist")
            return redirect("/register/")
        user = authenticate(username=user_name, password=password)
        if user is None:
            messages.error(request, "Invalid password")
            return redirect("/register/")
        else:
            login(request, user=user)
            return redirect("/")
    return render(request, "login.html")


def register_page(request):
    if request.method=="POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        user_name = request.POST.get("user_name")
        password = request.POST.get("password")
        user = User.objects.filter(username = user_name)
        if user.exists():
            messages.error(request, "Username Already taken")
            return redirect("/register/")
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=user_name
        )
        user.set_password(password)
        user.save()
        messages.success(request, "Account Created Successfully")
        return redirect("/login/")

    return render(request, "register.html")


def logout_page(request):
    logout(request)
    return redirect("/login/")