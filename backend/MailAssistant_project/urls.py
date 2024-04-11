"""
Mail Assistant Project URL Configuration.
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("MailAssistant/", include("MailAssistant.urls")),
    # ----------------------- SECURITY -----------------------#
    path("reset_password/", views.PasswordResetView.as_view(), name="reset_password"),
    path("reset_password_sent/", views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset_password_complete", views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
