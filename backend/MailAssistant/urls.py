from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from MailAssistant import microsoft_api
from MailAssistant import google_api


app_name = 'MailAssistant'

urlpatterns = [
    ######################## Actuals URLs ########################
    path('', views.home_page, name="home_page"),
    path('message/', views.get_message, name='get_message'), # TO TEST
    path('user/categories/', views.get_user_categories, name='user-categories'),
    path('user/emails/', views.get_user_emails, name='user-emails'),
    # path('user/emails/<int:email_id>/bullet-points/', views.get_email_bullet_points, name='email-bullet-points'),
    path('user/emails/<int:email_id>/mark-read/', views.set_email_read, name='email-mark-read'),
    path('user/emails/<int:email_id>/mark-reply-later/', views.set_email_reply_later, name='email-mark-reply-later'),
    path('user/emails/<int:email_id>/block-sender/', views.set_rule_block_for_sender, name='block-sender-via-email'),
    path('user/preferences/bg_color/', views.get_user_bg_color, name='get_user_bg_color'),
    path('user/preferences/set_bg_color/', views.set_user_bg_color, name='set_bg_color'),
    path('user/preferences/username/', views.get_user_details, name='get_user_details'),
    path('user/preferences/update-username/', views.update_username, name='update_username'),
    path('user/preferences/update-password/', views.update_password, name='update_password'),
    path('user/rules/', views.get_user_rules, name='get_user_rules'),
    path('user/create-rule/', views.create_user_rule, name='create_user_rule'),
    path('api/login/', views.login, name='login'), 
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', views.refresh_token, name='refresh_token'),
    path('api/authenticate-service', views.authenticate_service_view, name='authenticate_service'),
    path('api/get_mail', views.get_mail_view, name='get_mail'),
    path('api/get_mail_by_id', views.get_mail_by_id_view, name='get_mail_by_id'),
    path('api/save_last_mail', views.save_last_mail_view, name='save_last_mail'),
    path('api/get_unique_email_senders', views.get_unique_email_senders_view, name='get_unique_email_senders_view'),
    path('api/create_sender', views.create_sender, name='create_sender'),
    path('api/get-category-id/<str:category_name>/', views.get_category_id, name='get_category_id'),
    path('api/find-user/', views.find_user_view, name='find-user'),  # Add your view to the urlpatterns
    path('api/find-user-ai/', views.find_user_view_ai, name='find-user-ai'),
    path('api/new_email_ai/', views.new_email_ai, name='new_email_ai'),
    path('api/new_email_recommendations/', views.new_email_recommendations, name='new_email_recommendations'),
    path('api/correct_email_language/', views.correct_email_language, name='correct_email_language'),
    path('api/check_email_copywriting/', views.check_email_copywriting, name='check_email_copywriting'),
    path('api/send_mails/', views.send_email, name="send_mails"),
    path('api/generate_email_response_keywords/', views.generate_email_response_keywords, name="generate_email_response_keywords"),
    path('api/generate_email_answer/', views.generate_email_answer, name="generate_email_answer"),
    path('api/get_answer_later_emails/', views.get_answer_later_emails, name="get_answer_later_emails"),
    path('api/delete_account/', views.delete_account, name='delete_account'),
    path('api/set_category/', views.set_category, name="set_category"),
    path('api/update_category/<str:currentName>/', views.update_category, name="update_category"),
    path('api/delete_category/<str:currentName>/', views.delete_category, name="delete_category"),
    #path('api/test_authenticate_service/', TestAuthenticateServiceView.as_view(), name='test_authenticate_service'),


    
    # Auth Full backend - register user
    path('signup/', views.signup, name="signup"),

    ######################## Azure AD - OUTLOOK API ########################
    # authentification
    path('microsoft/auth_url/', microsoft_api.generate_auth_url, name='microsoft_auth_url'),
    # requests URLs
    path('microsoft/unread_mails/', microsoft_api.unread_mails, name='microsoft_unread_mails'),
    path('microsoft/get_parsed_contacts/', microsoft_api.get_parsed_contacts, name='microsoft_get_parsed_contacts'),
    path('microsoft/get_profile_image/', microsoft_api.get_profile_image, name='microsoft_get_profile_image'),
    path('microsoft/send_email/', microsoft_api.send_email, name='microsoft_send_email'),
    

    ######################## GOOGLE GMAIL API ########################
    # authentification
    path('google/auth_url/', google_api.generate_auth_url, name='google_auth_url'),
    # requests URLs
    path('gmail/unread_mails/', google_api.unread_mails, name='unread_mails'),
    path('gmail/get_parsed_contacts/', google_api.get_parsed_contacts, name='get_parsed_contacts'),
    path('gmail/get_profile_image/', google_api.get_profile_image, name='get_profile_image'),
]