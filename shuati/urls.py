from django.contrib import admin
from django.conf import settings  ##新增
from django.conf.urls import include
from django.urls import re_path as url
from django.contrib import admin
from django.urls import re_path, path
from django.views import static  ##新增
from django.views.static import serve

from shuati import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path("",views.index,name="index"),
    path('shuati_app/', include('shuati_app.urls')),



    re_path(r'^static/(?P<path>.*)$', static.serve,
        {'document_root': settings.STATIC_ROOT}, name='static'),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

# handler404 = views.page_not_found
# handler500 = views.server_error
# handler400 = views.bad_request
