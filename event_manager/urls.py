"""
    PROJEKT URLS

    http://127.0.0.1:8000/firstapp/first
    http://127.0.0.1:8000/company => Company App
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('firstapp/', include('first_app.urls')),
    path('', include('company.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls))
    ] + urlpatterns
