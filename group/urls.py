from django.urls import path

app_name = 'group' 

urlpatterns = [
    
    path('<int:group_id>/', group_detail, name='group_detail'),
    path('<int:group_id>/idea_create/', idea_create, name='idea_create'),
    path('<int:group_id>/idea_modify/<int:idea_id>/', idea_modify, name='idea_modify'),
    
]
