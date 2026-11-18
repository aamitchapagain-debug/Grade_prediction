from django.contrib import admin
from django.urls import path
from predictor import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.predict_grade, name="predict_grade"),
    path("history/", views.history, name="history"),
]
