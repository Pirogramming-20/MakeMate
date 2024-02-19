from django.urls import path
from .views import *

app_name = "preresult"

urlpatterns = [
    path("<int:group_id>/admin/", preresult, name="preresult"),
    path("<int:group_id>/", member_preresult, name="member_preresult"),
    path(
        "<int:group_id>/admin/modify",
        preresult_modify,
        name="preresult_modify",
    ),
    path(
        "<int:group_id>/admin/vote1/preresult/select",
        first_vote_select,
        name="first_vote_select",
    ),
    path(
        "<int:group_id>/admin/vote1/preresult/unselect",
        first_vote_unselect,
        name="first_vote_unselect",
    ),
    path(
        "<int:group_id>/admin/vote2/preresult/select",
        second_vote_select,
        name="second_vote_select",
    ),
    path(
        "<int:group_id>/admin/vote2/preresult/unselect",
        second_vote_unselect,
        name="second_vote_unselect",
    ),
]
