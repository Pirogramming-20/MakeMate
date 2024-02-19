from django.urls import path
from .views import *

app_name = "group_admin"

urlpatterns = [
    path("<int:group_id>/", admin_page, name="admin_page"),
    path(
        "<int:group_id>/user_delete/<int:user_id>/",
        group_user_delete,
        name="user_delete",
    ),
    path(
        "<int:group_id>/user_update/<int:user_id>/",
        group_user_update,
        name="user_update",
    ),
    path("<int:group_id>/admin_add/", admin_add, name="admin_add"),
    path("<int:group_id>/admin_delete/",
         admin_delete,
         name="admin_delete"),
    path("<int:group_id>/idea_delete/<int:user_id>/", admin_idea_delete, name="admin_idea_delete")
]