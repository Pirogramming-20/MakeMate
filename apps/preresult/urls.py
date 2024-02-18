from django.urls import path
from .views import *

app_name = "preresult"

urlpatterns = [
    path("<int:group_id>/admin/", preresult, name="preresult"),
    path("<int:group_id>/",
         member_preresult,
         name="member_preresult"),
    path(
        "<int:group_id>/admin/modify",
        preresult_modify,
        name="preresult_modify",
    ),
]