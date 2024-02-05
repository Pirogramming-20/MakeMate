from django.urls import path
from .views import group_base_info, group_detail_info, group_date, share, check_nonadmin, check_admin, info_nonadmin, group_detail, idea_create, idea_modify, idea_delete, idea_detail, vote_create 

app_name = 'group'

urlpatterns = [
    path('base_set/', group_base_info, name='base_set'),
    path('detail_set/', group_detail_info, name='detail_set'),
    path('date_set/', group_date, name='date_set'),
    path('share/', share, name='share'),
    path('<int:group_id>/password_check/', check_nonadmin, name='check_nonadmin'),
    path('<int:group_id>/admin/password_check/', check_admin, name='check_admin'),
    path('<int:group_id>/non_admin_info/', info_nonadmin, name='info_nonadmin'),
    path('<int:group_id>/', group_detail, name='group_detail'),
    path('<int:group_id>/idea_create/', idea_create, name='idea_create'),
    path('<int:group_id>/idea_modify/<int:idea_id>/', idea_modify, name='idea_modify'),
    path('<int:group_id>/idea_delete/<int:idea_id>/', idea_delete, name='idea_delete'),
    path('<int:group_id>/idea_detail/<int:idea_id>/', idea_detail, name='idea_detail'),
    path('<int:group_id>/idea_vote/', vote_create, name='group_vote_create'),

]
