"""
Mail Assistant Project URL Configuration.
"""

from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("MailAssistant/", include("aomail.urls")),
]
