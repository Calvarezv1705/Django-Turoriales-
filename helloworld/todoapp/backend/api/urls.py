from django.urls import path
from . import views

urlpatterns = [
    path('todos/', views.ToDoList.as_view(), name='list'),
]
