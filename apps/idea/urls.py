from django.urls import path
from .views import *

app_name = "idea"

urlpatterns = [
    path("<int:group_id>/create/", idea_create, name="idea_create"),
    path("<int:group_id>/modify/<int:idea_id>/",
         idea_modify,
         name="idea_modify"),
    path("<int:group_id>/delete/<int:idea_id>/",
         idea_delete,
         name="idea_delete"),
    path("<int:group_id>/detail/<int:idea_id>/",
         idea_detail,
         name="idea_detail"),
    path(
        "<int:group_id>/download/<int:idea_id>/",
        idea_download,
        name="idea_download",
    ),
]