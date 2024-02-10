from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

app_name = "group"

urlpatterns = [

    path("base_set/", group_base_info, name="base_set"),
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
    path("<int:group_id>/admin/", admin_page, name="admin_page"),
    path("<int:group_id>/admin/user_delete/<int:user_id>",group_user_delete, name="user_delete"),
    path("<int:group_id>/admin/user_update/<int:user_id>",group_user_update, name="user_update"),
    path("<int:group_id>/admin/admin_add", admin_add, name="admin_add"),
    path("<int:group_id>/admin/admin_delete", admin_delete, name="admin_delete"),
    path('<int:group_id>/', group_detail, name='group_detail'),
    path('<int:group_id>/idea_create/', idea_create, name='idea_create'),
    path('<int:group_id>/idea_modify/<int:idea_id>/', idea_modify, name='idea_modify'),
    path('<int:group_id>/idea_delete/<int:idea_id>/', idea_delete, name='idea_delete'),
    path('<int:group_id>/idea_detail/<int:idea_id>/', idea_detail, name='idea_detail'),
    path('<int:group_id>/idea_vote/', vote_create, name='group_vote_create'),
    path('<int:group_id>/idea_vote_modify/', vote_modify, name='vote_modify'),
    path('<int:group_id>/idea_download/<int:idea_id>/', idea_download, name='idea_download'),
    path('<int:group_id>/preresult/modify', preresult_modify, name='preresult_modify'),
    path('<int:group_id>/result/', result, name='result'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)