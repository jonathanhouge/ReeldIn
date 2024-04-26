from django.urls import path
from . import views

app_name = "recommendations"

urlpatterns = [
    path("", views.index, name="index"),
    path("narrow/", views.narrow_view, name="narrow"),
    path("recommend/", views.recommend_view, name="recommend"),
    path("delete/", views.delete_view, name="delete"),
]
