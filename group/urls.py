from django.urls import path
from .views import check_nonadmin, check_admin, info_nonadmin

app_name = 'group'

urlpatterns = [
    path('<int:group_id>/password_check/', check_nonadmin, name='check_nonadmin'),
    path('<int:group_id>/admin/password_check', check_admin, name='check_admin'),
    path('<int:group_id>/non_admin_info/', info_nonadmin, name='info_nonadmin')
]
