from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

app_name = "result"

urlpatterns = [
    path("<int:group_id>/", result, name="result"),
    path("<int:group_id>/team_building/",
         start_team_building,
         name="team_building"),
]
