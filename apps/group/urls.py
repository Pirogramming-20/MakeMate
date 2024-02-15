from django.urls import path
from .views import *

app_name = "group"

urlpatterns = [
    path("<int:group_id>/", group_detail, name="group_detail"),
    path("<int:group_id>/result/", result, name="result"),
]
