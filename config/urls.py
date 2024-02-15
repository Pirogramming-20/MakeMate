from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.common.urls')),
    path('group/', include('apps.group.urls')),
    path('group_admin/', include('apps.group_admin.urls')),
    path('group_setting/', include('apps.group_setting.urls')),
    path('preresult/', include('apps.preresult.urls')),
    path('idea/', include('apps.idea.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)