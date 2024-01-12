from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("create-standalone/", views.create_standalone, name="create-standalone"),
    path("initial-funds/<str:receiver>/", views.initial_funds, name="initial-funds"),
    path("transfer-funds/<str:sender>/", views.transfer_funds, name="transfer-funds"),
]