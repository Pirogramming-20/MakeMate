from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.common.urls")),
    path("group/", include("apps.group.urls")),
    path("group_admin/", include("apps.groupAdmin.urls")),
    path("setting/", include("apps.groupSetting.urls")),
    path("preresult/", include("apps.preresult.urls")),
    path("result/", include("apps.result.urls")),
    path("idea/", include("apps.idea.urls")),
    path("vote/", include("apps.vote.urls")),
]
