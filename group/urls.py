from django.urls import path
from .views import group_base_info, group_share, check_nonadmin, check_admin, info_nonadmin, preresult

app_name = 'group'

urlpatterns = [
    path('base_set/', group_base_info, name='base_set'),
    path('share/<int:group_id>', group_share, name='share'),
    path('<int:group_id>/password_check/', check_nonadmin, name='check_nonadmin'),
    path('<int:group_id>/admin/password_check/', check_admin, name='check_admin'),
    path('<int:group_id>/non_admin_info/', info_nonadmin, name='info_nonadmin'),
    path('<int:group_id>/preresult/', preresult, name='preresult'),
]
