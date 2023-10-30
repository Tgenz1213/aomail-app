from django.urls import path
from . import views
from MailAssistant import microsoft_api
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'MailAssistant'

urlpatterns = [
    path('', views.home_page, name="home_page"),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('register/', views.register, name="register"),
    path('send_mails/', views.send_mail, name="send_mails"),
    path('authenticate/', microsoft_api.authenticate_service, name='authenticate_service'),
    path('callback/', microsoft_api.handle_callback, name='handle_callback'),
    path('message/', views.get_message, name='get_message'), # THEO TEST
    path('user/categories/', views.get_user_categories, name='user-categories'),
    path('user/emails/', views.get_user_emails, name='user-emails'),
    # path('user/emails/<int:email_id>/bullet-points/', views.get_email_bullet_points, name='email-bullet-points'),
    path('user/emails/<int:email_id>/mark-read/', views.set_email_read, name='email-mark-read'),
    path('user/emails/<int:email_id>/mark-reply-later/', views.set_email_reply_later, name='email-mark-reply-later'),
    path('user/emails/<int:email_id>/block-sender/', views.set_rule_block_for_sender, name='block-sender-via-email'),
    path('user/preferences/bg_color/', views.get_user_bg_color, name='get_user_bg_color'),
    path('api/login/', views.login, name='login'), # MADE BY THEO
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


]
