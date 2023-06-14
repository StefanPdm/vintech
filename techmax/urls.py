from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from django.conf import settings
from django.views.static import serve
from django.urls import re_path as url


urlpatterns = [path("admin/", admin.site.urls), path("", include("shop.urls"))]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# urlpatterns = [
#   url(r'^static/img/produkte/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
#   url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
#   path("admin/", admin.site.urls), path("", include("shop.urls"))
# ]

handler404 = "shop.views.handler404"