from django.urls import path
from .views import group_base_info

app_name = 'group'

urlpatterns = [
    path('base_set/', group_base_info, name='base_set')
]
