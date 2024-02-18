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
    path("<int:group_id>/admin/vote1/preresult",
         vote1_preresult,
         name="vote1_preresult"),
    path("<int:group_id>/admin/vote1/preresult/select",
         vote1_select,
         name="vote1_select"),
    path(
        "<int:group_id>/admin/vote1/preresult/unselect",
        vote1_unselect,
        name="vote1_unselect",
    ),
]
