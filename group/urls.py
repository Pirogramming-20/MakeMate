from django.urls import path

from .views import group_base_info, group_share, check_nonadmin, check_admin, info_nonadmin, preresult, admin_page, group_user_delete, group_user_update, admin_add, admin_delete,

app_name = "group"

urlpatterns = [

    path("base_set/", group_base_info, name="base_set"),
    path("detail_set/", group_detail_info, name="detail_set"),
    path("date_set/", group_date, name="date_set"),
    path("share/", share, name="share"),
    path("<int:group_id>/password_check/",
         check_nonadmin,
         name="check_nonadmin"),
    path("<int:group_id>/admin/password_check/",
         check_admin,
         name="check_admin"),
    path("<int:group_id>/non_admin_info/", info_nonadmin,
         name="info_nonadmin"),
    path('base_set/', group_base_info, name='base_set'),
    path('share/<int:group_id>', group_share, name='share'),
    path('<int:group_id>/password_check/', check_nonadmin, name='check_nonadmin'),
    path('<int:group_id>/admin/password_check/', check_admin, name='check_admin'),
    path('<int:group_id>/non_admin_info/', info_nonadmin, name='info_nonadmin'),
    path('<int:group_id>/preresult/', preresult, name='preresult'),
    path("<int:group_id>/admin", admin_page, name="admin_page"),
    path("<int:group_id>/admin/user_delete/<int:user_id>",group_user_delete, name="user_delete"),
    path("<int:group_id>/admin/user_update/<int:user_id>",group_user_update, name="user_update"),
    path("<int:group_id>/admin/admin_add", admin_add, name="admin_add"),
    path("<int:group_id>/admin/admin_delete", admin_delete, name="admin_delete"),
]
