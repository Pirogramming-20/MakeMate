from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

app_name = "idea"

urlpatterns = [
    path("<int:group_id>/idea_create/", idea_create, name="idea_create"),
    path("<int:group_id>/idea_modify/<int:idea_id>/",
         idea_modify,
         name="idea_modify"),
    path("<int:group_id>/idea_delete/<int:idea_id>/",
         idea_delete,
         name="idea_delete"),
    path("<int:group_id>/idea_detail/<int:idea_id>/",
         idea_detail,
         name="idea_detail"),
    path("<int:group_id>/idea_vote/", vote_create, name="group_vote_create"),
    path(
        "<int:group_id>/idea_download/<int:idea_id>/",
        idea_download,
        name="idea_download",
    ),
]