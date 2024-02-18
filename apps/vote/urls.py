from django.urls import path
from .views import *

app_name = "vote"

urlpatterns = [
    path("<int:group_id>/idea_vote/", vote_create, name="vote_create"),
    path("<int:group_id>/idea_modify/", vote_modify, name="vote_modify"),
]