from django.urls import path

from . import views

urlpatterns = [
    path("",views.index),
    path("api/todolist/",views.todolist),
    path("api/add/",views.todoadd),
    path("api/update/<int:todoid>/",views.todoupdate),
    path("api/del/<int:todoid>/",views.tododel),

    path("login/", views.mylogin),
    path("logout/", views.mylogout),
    path("register/", views.register),
]


