from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="homepage"),
    path('recipes/<int:recipe_id>/', views.recipe_detail_view, name="recipedetails"),
    path('recipes/<int:recipe_id>/edit/', views.edit_recipe,
         name="editrecipe"),
    path('author/<str:author_name>/', views.author_detail_view, name="author"),
    path('addrecipe/', views.add_recipe, name="addrecipe"),
    path('addauthor/', views.add_author, name="addauthor"),
    path('favorite/<int:recipe_id>/', views.add_favorite, name="addfavorite"),
    path('unfavorite/<int:recipe_id>/', views.remove_favorite,
         name="removefavorite"),
    path('signup/', views.signup_view, name="signupview"),
    path('login/', views.login_view, name="loginview"),
    path('logout/', views.logout_view, name="logoutview")

]