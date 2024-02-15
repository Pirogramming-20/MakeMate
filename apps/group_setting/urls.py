from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

app_name = "group_setting"

urlpatterns = [
    path("", group_base_info, name="base_set"),
    path("<int:group_id>/",
         check_nonadmin,
         name="check_nonadmin"),
    path("<int:group_id>/admin/",
         check_admin,
         name="check_admin"),
    path("<int:group_id>/non_admin_info/", info_nonadmin,
         name="info_nonadmin"),
    path("share/<int:group_id>", group_share, name="share"),
]