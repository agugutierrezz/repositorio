from django.contrib import admin
from django.urls import include, path
from django.conf import settings

import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path("polls/", include("polls.urls")),
]

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]