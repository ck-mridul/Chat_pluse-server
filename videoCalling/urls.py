from django.urls import path 
from . import views

urlpatterns = [
    path('createroom/', views.CreateRommView.as_view())
]