from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

app_name = "group"

urlpatterns = [
    path("base_set/", group_base_info, name="base_set"),
    path("share/<int:group_id>", group_share, name="share"),
    path("<int:group_id>/password_check/",
         check_nonadmin,
         name="check_nonadmin"),
    path("<int:group_id>/admin/password_check/",
         check_admin,
         name="check_admin"),
    path("<int:group_id>/non_admin_info/", info_nonadmin,
         name="info_nonadmin"),
    path("<int:group_id>/admin/preresult/", preresult, name="preresult"),
    path("<int:group_id>/preresult/",
         member_preresult,
         name="member_preresult"),
    path("<int:group_id>/admin/", admin_page, name="admin_page"),
    path(
        "<int:group_id>/admin/user_delete/<int:user_id>",
        group_user_delete,
        name="user_delete",
    ),
    path(
        "<int:group_id>/admin/user_update/<int:user_id>",
        group_user_update,
        name="user_update",
    ),
    path("<int:group_id>/admin/admin_add", admin_add, name="admin_add"),
    path("<int:group_id>/admin/admin_delete",
         admin_delete,
         name="admin_delete"),
    path("<int:group_id>/", group_detail, name="group_detail"),
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
    path("<int:group_id>/idea_vote/", vote_create, name="vote_create"),
    path("<int:group_id>/idea_modify/", vote_modify, name="vote_modify"),
    path(
        "<int:group_id>/idea_download/<int:idea_id>/",
        idea_download,
        name="idea_download",
    ),
    path(
        "<int:group_id>/admin/preresult/modify",
        preresult_modify,
        name="preresult_modify",
    ),
    path("<int:group_id>/result/", result, name="result"),
    path("<int:group_id>/team_building/",
         start_team_building,
         name="team_building"),
    path(
        "<int:group_id>/admin/idea_delete/<int:user_id>/",
        admin_idea_delete,
        name="admin_idea_delete",
    ),
    # 요청으로 실행시킬게 아니라 일단 주석처리했습니다!
    # path("<int:group_id>/team_building/",
    # start_team_building,
    # name="team_building"),
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

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
