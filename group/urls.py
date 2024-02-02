from django.urls import path
from .views import group_base_info, group_detail_info, group_date, share, check_nonadmin, check_admin, info_nonadmin

app_name = 'group'

urlpatterns = [
    path('base_set/', group_base_info, name='base_set'),
    path('detail_set/', group_detail_info, name='detail_set'),
    path('date_set/', group_date, name='date_set'),
    path('share/<int:group_id>/', share, name='share'),
    path('<int:group_id>/password_check/', check_nonadmin, name='check_nonadmin'),
    path('<int:group_id>/admin/password_check/', check_admin, name='check_admin'),
    path('<int:group_id>/non_admin_info/', info_nonadmin, name='info_nonadmin')
]
