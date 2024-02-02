from django.urls import path
from .views import group_base_info, group_detail_info, group_date

app_name = 'group'

urlpatterns = [
    path('base_set/', group_base_info, name='base_set'),
    path('detail_set/', group_detail_info, name='detail_set'),
    path('date_set/', group_date, name='date_set'),
]
