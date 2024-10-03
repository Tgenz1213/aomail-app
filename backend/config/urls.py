"""
Aomail Project base URL Configuration.
"""

from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("aomail/", include("aomail.urls")),
]
