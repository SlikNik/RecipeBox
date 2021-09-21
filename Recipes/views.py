from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .models import Author, Recipe
from .forms import SignupForm, LoginForm, AddAuthorForm, AddRecipeForm


def index(request):
    all_recipes = Recipe.objects.all()
    return render(request, 'index.html', {'recipes': all_recipes})

def author_detail_view(request, author_name):
    current_author = Author.objects.filter(name=author_name).first()
    author_recipes = Recipe.objects.filter(author=current_author)
    author_favorites =  Recipe.objects.filter(favorites=current_author.user)
    return render(request, 'author_detail.html', {'author': current_author, 'recipes': author_recipes, 
                  'favorites': author_favorites})

def recipe_detail_view(request, recipe_id):
    current_recipe = Recipe.objects.filter(id=recipe_id).first()
    favorites = current_recipe.favorites.all()
    return render(request, 'recipe_detail.html', {'recipe': current_recipe, 'favorites': favorites})

@login_required
def add_author(request):
    if request.user.is_staff:
        if request.method == 'POST':
            form = AddAuthorForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('homepage'))
        form = AddAuthorForm()
        return render(request, 'forms/author_form.html', {'form': form,  'author': 'active'})
    else:
        return render(request, 'no_access.html', {'user': request.user})


@login_required
def add_recipe(request):
    if request.user.is_staff:
        if request.method == 'POST':
            form = AddRecipeForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('homepage'))
        form = AddRecipeForm()
        return render(request, 'forms/recipe_form.html', {'form': form, 'type': 'recipe'})
    else:
        if request.method == 'POST':
            form = AddRecipeForm(request.POST)
            if form.is_valid(): 
                form.non_staff()
                form.save()
                return HttpResponseRedirect(reverse('homepage'))
        form = AddRecipeForm(initial={'author': request.user.author})
        return render(request, 'forms/recipe_form.html', {'form': form, 'type': 'recipe'})

@login_required
def edit_recipe(request, recipe_id):
    current_recipe = Recipe.objects.get(id=recipe_id)
    if request.user.is_staff:
        if request.method == 'POST':
            form = AddRecipeForm(request.POST)
            if form.is_valid():
                new_recipe = form.cleaned_data
                current_recipe.title = new_recipe['title']
                current_recipe.description = new_recipe['description']
                current_recipe.required_time = new_recipe['required_time']
                current_recipe.instructions = new_recipe['instructions']
                current_recipe.save()
            return HttpResponseRedirect(reverse('recipedetails',
                                        args=[current_recipe.id]))
    else:
        if request.user == current_recipe.author.user:
            if request.method == 'POST':
                form = AddRecipeForm(request.POST)
                if form.is_valid():
                    form.non_staff()
                    new_recipe = form.cleaned_data
                    current_recipe.title = new_recipe['title']
                    current_recipe.description = new_recipe['description']
                    current_recipe.required_time = new_recipe['required_time']
                    current_recipe.instructions = new_recipe['instructions']
                    current_recipe.save()
                return HttpResponseRedirect(reverse('recipedetails',
                                            args=[current_recipe.id]))
        else:
            return render(request, 'no_access.html', {'user': request.user})
    form = AddRecipeForm(initial={'title': current_recipe.title,
                                  'description': current_recipe.description,
                                  'author': current_recipe.author,
                                  'required_time': current_recipe.required_time,
                                  'instructions': current_recipe.instructions})
    return render(request, 'forms/recipe_form.html', {'form': form, 'type': 'recipe'})


@login_required
def add_favorite(request, recipe_id):
    current_user = User.objects.get(id=request.user.id)
    current_recipe = Recipe.objects.get(id=recipe_id)
    current_recipe.favorites.add(current_user)
    favorites = current_recipe.favorites.all()
    return render(request, 'recipe_detail.html', {'recipe': current_recipe, 'favorites': favorites})


@login_required
def remove_favorite(request, recipe_id):
    current_user = User.objects.get(id=request.user.id)
    current_recipe = Recipe.objects.get(id=recipe_id)
    current_recipe.favorites.remove(current_user)
    favorites = current_recipe.favorites.all()
    return render(request, 'recipe_detail.html', {'recipe': current_recipe, 'favorites': favorites})

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        author_form = AddAuthorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            name = data.get('first_name').lower() + data.get('last_name').lower()
            new_user = User.objects.create(username=name, email=data.get('email'), password=data.get('password'))
            new_user.save()
            Author.objects.create(name=data.get('first_name').capitalize() + ' ' + data.get('last_name').capitalize(), bio=data.get('bio'), user=new_user)
            login(request, new_user)
            return HttpResponseRedirect(reverse('homepage'))

    form = SignupForm()                      
    return render(request, 'forms/signup_form.html',  {'form': form, 'type': 'signup'})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            custom_user = authenticate(request, username=data.get('username'), password=data.get('password'))
            if custom_user:
                login(request, custom_user)
                # return HttpResponseRedirect(reverse('homepage'))
                return HttpResponseRedirect(request.GET.get( 'next',reverse('homepage')))
      
    form = LoginForm()
    return render(request, 'forms/login_form.html', {'form': form, 'type': 'login'})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))

                