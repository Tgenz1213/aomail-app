"""
Django Rest Framework (DRF) URL Configuration for MailAssistant RESTful API.
"""

from django.urls import path
from MailAssistant.email_providers import google_api, microsoft_api
from . import views


app_name = 'MailAssistant'

urlpatterns = [
    #----------------------- ACCOUNT -----------------------#
    path("reset_password/<token>/", views.reset_password, name="reset_password"), # dev
    path("generate_reset_token/", views.generate_reset_token, name="generate_reset_token"), # dev

    path('api/is_authenticated/', views.is_authenticated, name='is_authenticated'), # ok
    path('api/login/', views.login, name='login'), # ok
    path('api/token/refresh/', views.refresh_token, name='refresh_token'), # ok
    path('api/delete_account/', views.delete_account, name='delete_account'), # ok
    path('user/preferences/update-username/', views.update_username, name='update_username'), # ok
    path('user/preferences/update-password/', views.update_password, name='update_password'), # ok
    path('user/preferences/bg_color/', views.get_user_bg_color, name='get_user_bg_color'), # ok
    path('user/preferences/set_bg_color/', views.set_user_bg_color, name='set_bg_color'), # ok
    path('signup/', views.signup, name='signup'), # ok
    path('check_username/', views.check_username, name='check_username'), # ok
    path('api/get_profile_image/', views.get_profile_image, name='get_profile_image'), # ok
    #----------------------- CATEGORIES -----------------------#
    path('api/create_category/', views.create_category, name='create_category'), # ok
    path('api/get-category-id/<str:category_name>/', views.get_category_id, name='get_category_id'), # ok
    path('api/update_category/<str:current_name>/', views.update_category, name='update_category'), # ok
    path('api/delete_category/<str:current_name>/', views.delete_category, name='delete_category'), # ok
    #----------------------- EMAIL ACCOUNT -----------------------#
    path('api/create_sender', views.create_sender, name='create_sender'), # ok
    path('api/check_sender', views.check_sender_for_user, name='check_sender_for_user'), # ok
    path('api/get_mail_by_id', views.get_mail_by_id, name='get_mail_by_id'), # ok
    #----------------------- USER -----------------------#
    path('user/categories/', views.get_user_categories, name='user-categories'), # ok
    path('user/emails/', views.get_user_emails, name='user-emails'), # ok
    path('user/emails/<int:email_id>/mark-read/', views.set_email_read, name='email-mark-read'), # ok
    path('user/emails/<int:email_id>/mark-unread/', views.set_email_undread, name='email-mark-unread'), # ok
    path('user/emails/<int:email_id>/mark-reply-later/', views.set_email_reply_later, name='email-mark-reply-later'), # ok
    path('user/emails/<int:email_id>/block-sender/', views.set_rule_block_for_sender, name='block-sender-via-email'), # ok
    path('user/contacts/', views.get_user_contacts, name='get_user_contacts'), # ok
    path('user/rules/', views.get_user_rules, name='get_user_rules'), # ok
    path('user/rules/<int:id_rule>/', views.get_user_rule_by_id, name='get_user_rule_by_id'), # ok
    path('user/delete-rules/<int:id_rule>/', views.delete_user_rule_by_id, name='delete_user_rule_by_id'), # ok
    path('user/create-rule/', views.create_user_rule, name='create_user_rule'), # ok
    path('user/update-rule/', views.update_user_rule, name='update_user_rule'), # ok
    path('user/emails/<int:email_id>/delete/', views.delete_email, name='email-delete'), # ok
    path('user/preferences/username/', views.get_user_details, name='get_user_details'), # ok
    path('user/emails_linked/', views.get_emails_linked , name='get_emails_linked'), # ok
    path('user/search_emails/', views.search_emails , name='search_emails'), # ok
    
    path('user/search_emails_ai/', views.search_emails_ai , name='search_emails_ai'), # dev

    path('user/social_api/unlink/', views.unlink_email, name='unlink_email'), # ok
    path('user/social_api/link/', views.link_email, name='link_email'), # ok
    path('user/social_api/update_user_description/', views.update_user_description, name='update_user_description'), # ok
    path('user/social_api/get_user_description/', views.get_user_description, name='get_user_description'), # ok
    # TODO: remove as we have stripe
    path('user/set_billing_informations/', views.set_user_billing_informations, name= 'set_user_billing_informations'), # dev
    #----------------------- ARTIFICIAL INTELLIGENCE -----------------------#
    path('api/find-user-ai/', views.find_user_view_ai, name='find-user-ai'), # ok
    path('api/new_email_ai/', views.new_email_ai, name='new_email_ai'), # ok
    path('api/new_email_recommendations/', views.new_email_recommendations, name='new_email_recommendations'), # ok
    path('api/improve_email_writing/', views.improve_email_writing, name='improve_email_writing'), # ok
    path('api/correct_email_language/', views.correct_email_language, name='correct_email_language'), # ok
    path('api/check_email_copywriting/', views.check_email_copywriting, name='check_email_copywriting'), # ok
    path('api/send_email/', views.send_email, name='send_email'), # ok
    path('api/generate_email_response_keywords/', views.generate_email_response_keywords, name='generate_email_response_keywords'), # ok
    path('api/generate_email_answer/', views.generate_email_answer, name='generate_email_answer'), # ok
    path('api/get_answer_later_emails/', views.get_answer_later_emails, name='get_answer_later_emails'), # ok
    #----------------------- OAuth 2.0 EMAIL PROVIDERS API -----------------------#
    path('microsoft/auth_url/', microsoft_api.generate_auth_url, name='microsoft_auth_url'), # ok
    path('microsoft/auth_url_link_email/', microsoft_api.auth_url_link_email, name='microsoft_auth_url_link_email'), # ok
    path('microsoft/receive_mail_notifications/', microsoft_api.MicrosoftEmailNotification.as_view(), name='receive_mail_notifications'), # ok
    path('microsoft/receive_contact_notifications/', microsoft_api.MicrosoftContactNotification.as_view(), name='receive_contact_notifications'), # ok
    path('microsoft/receive_subscription_notifications/', microsoft_api.MicrosoftSubscriptionNotification.as_view(), name='receive_subscription_notifications'), # ok
    path('google/auth_url/', google_api.generate_auth_url, name='google_auth_url'), # ok
    path('google/auth_url_link_email/', google_api.auth_url_link_email, name='google_auth_url_link_email'), # dev
    path('google/receive_mail_notifications/', google_api.receive_mail_notifications, name='google_receive_mail_notifications'), # ok
    #----------------------- PAYMENT PROVIDER API -----------------------#
    path('stripe/receive_payment_notifications/', views.receive_payment_notifications, name='stripe_receive_payment_notifications'), # dev
    #----------------------- TESTING URLs -----------------------#
    # path('api/save_last_mail', views.save_last_mail_view, name='save_last_mail'), # testing
    # path('api/save_last_mail_outlook', views.save_last_mail_outlook, name='save_last_mail_outlook'), # testing
    #----------------------- UNUSED URLs -----------------------#
    # path('api/get_mail', views.get_mail_view, name='get_mail'), # testing just to get the first email
    # path('api/authenticate-service', views.authenticate_service_view, name='authenticate_service'), # testing
    # path('api/get_parsed_contacts/', views.get_parsed_contacts, name='get_parsed_contacts'),
    # path('api/get_unique_email_senders', views.è, name='get_unique_email_senders_view'),
    # path('user/emails/<int:email_id>/bullet-points/', views.get_email_bullet_points, name='email-bullet-points'),
    # path('user/emails/<int:email_id>/delete/', views.delete_email, name='email-delete'),
    # path('api/find-user/', views.find_user_view, name='find-user'),
    # path('api/unread_mails/', views.unread_mails, name='unread_mails'),    
    #path('api/get_first_email/', views.get_first_email, name='get_first_email'), # ok
]