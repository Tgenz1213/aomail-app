"""
Django Rest Framework (DRF) URL Configuration for Aomail RESTful API.
"""

from django.urls import path
from aomail.email_providers.google import authentication as auth_google
from aomail.email_providers.google import webhook as webhook_google
from aomail.email_providers.microsoft import authentication as auth_microsoft
from aomail.email_providers.microsoft import webhook as webhook_microsoft
from aomail.controllers import artificial_intelligence as ai
from aomail.controllers import authentication as auth
from aomail.controllers import preferences as prefs
from aomail.controllers import categories, filters, rules, emails, search_emails
from aomail.controllers import statistics
from aomail.controllers import search_labels
from aomail.controllers import labels
from .controllers import views


urlpatterns = [
    #----------------------- AUTHENTICATION -----------------------#
    path("generate_reset_token/", auth.generate_reset_token, name="generate_reset_token"), # ok
    path("reset_password/<str:uidb64>/<str:token>/", auth.reset_password, name="reset_password"), # ok
    path('api/is_authenticated/', auth.is_authenticated, name='is_authenticated'), # ok
    path('api/login/', auth.login, name='login'), # ok
    path('api/token/refresh/', auth.refresh_token, name='refresh_token'), # ok
    path('api/delete_account/', auth.delete_account, name='delete_account'), # ok
    path('signup/', auth.signup, name='signup'), # ok
    path('check_username/', auth.check_username, name='check_username'), # ok
    path('user/social_api/unlink/', auth.unlink_email, name='unlink_email'), # ok
    path('user/social_api/link/', auth.link_email, name='link_email'), # ok
    #----------------------- CATEGORIES -----------------------#
    path('user/categories/', categories.get_user_categories, name='get_user_categories'), # ok
    path('api/create_category/', categories.create_category, name='create_category'), # ok
    path('api/get_category_id/', categories.get_category_id, name='get_category_id'), # ok
    path('api/update_category/', categories.update_category, name='update_category'), # ok
    path('api/delete_category/', categories.delete_category, name='delete_category'), # ok
    path('api/get_rules_linked/', categories.get_rules_linked, name='get_rules_linked'), # ok
    #----------------------- FILTERS -----------------------#
    path('user/filters/', filters.get_user_filter, name='get_user_filters'),
    path('api/create_filter/', filters.create_filter, name='create_filter'),
    path('api/update_filter/', filters.update_filter, name='update_filter'),
    path('api/delete_filter/', filters.delete_filter, name='delete_filter'),
    #----------------------- RULES -----------------------#
    path('user/rules/', rules.get_user_rules, name='get_user_rules'), # ok
    path('user/rules/<int:id_rule>/', rules.get_user_rule_by_id, name='get_user_rule_by_id'), # ok
    path('user/delete_rules/<int:id_rule>/', rules.delete_user_rule_by_id, name='delete_user_rule_by_id'), # ok
    path('user/create_rule/', rules.create_user_rule, name='create_user_rule'), # ok
    path('user/update_rule/', rules.update_user_rule, name='update_user_rule'), # ok
    path('user/emails/<int:email_id>/block_sender/', rules.set_rule_block_for_sender, name='set_rule_block_for_sender'), # ok
    #----------------------- PREFERENCES -----------------------#
    path('user/preferences/update_username/', prefs.update_username, name='update_username'), # ok
    path('user/preferences/update_password/', prefs.update_password, name='update_password'), # ok
    path('user/preferences/language/', prefs.get_user_language, name='get_user_language'), # ok
    path('user/preferences/set_language/', prefs.set_user_language, name='set_user_language'), # ok
    path('user/preferences/theme/', prefs.get_user_theme, name='get_user_theme'), # ok
    path('user/preferences/set_theme/', prefs.set_user_theme, name='set_user_theme'), # ok
    path('user/preferences/timezone/', prefs.get_user_timezone, name='get_user_timezone'), # ok
    path('user/preferences/set_timezone/', prefs.set_user_timezone, name='set_user_timezone'), # ok
    path('user/preferences/username/', prefs.get_user_details, name='get_user_details'), # ok
    #----------------------- EMAILS -----------------------#
    path('user/emails/delete_emails', emails.delete_emails, name='delete_emails'), # waiting for implementation in FE
    path('user/emails/<int:email_id>/archive/', emails.archive_email, name='archive_email'), # waiting for implementation in FE
    
    path('user/emails_ids/', search_emails.get_user_emails_ids, name='get_user_emails'), # ok
    path('user/get_email_content/', search_emails.get_email_content, name='get_email_content'), # ok
    path('user/get_emails_data/', search_emails.get_emails_data, name='get_emails_data'), # ok
    path('user/get_first_email/', emails.get_first_email, name='get_first_email'), # ok
    path('user/emails/<int:email_id>/mark_read/', emails.set_email_read, name='set_email_read'), # ok
    path('user/emails/<int:email_id>/mark_unread/', emails.set_email_unread, name='set_email_unread'), # ok
    path('user/emails/<int:email_id>/mark_reply_later/', emails.set_email_reply_later, name='set_email_reply_laterr'), # ok
    path('user/emails/<int:email_id>/unmark_reply_later/', emails.set_email_not_reply_later, name='set_email_not_reply_later'), # ok
    path('user/emails/<int:email_id>/attachments/<str:attachment_name>/', emails.retrieve_attachment_data, name='retrieve_attachment_data'), 
    path('api/get_mail_by_id', emails.get_mail_by_id, name='get_mail_by_id'), # ok
    path('user/emails/<int:email_id>/delete/', emails.delete_email, name='delete_email'), # ok
    #----------------------- VIEWS -----------------------#
    path('pictures/<path:image_name>', views.serve_image, name='serve_image'), # dev
    path('user/get_batch_emails/', views.get_batch_emails, name='get_batch_emails'), # dev

    path('user/contacts/', views.get_user_contacts, name='get_user_contacts'), # ok
    path('user/emails_linked/', views.get_emails_linked , name='get_emails_linked'), # ok
    path('user/search_emails/', views.search_emails , name='search_emails'), # ok
    path('user/social_api/send_email/', views.send_email, name='send_email'), # ok
    path('user/social_api/send_schedule_email/', views.send_schedule_email, name='send_schedule_email'), # ok
    path('user/social_api/get_profile_image/', views.get_profile_image, name='get_profile_image'), # ok
    path('user/social_api/update_user_description/', views.update_user_description, name='update_user_description'), # ok
    path('user/social_api/get_user_description/', views.get_user_description, name='get_user_description'), # ok
    path('api/create_sender', views.create_sender, name='create_sender'), # ok
    path('api/check_sender', views.check_sender_for_user, name='check_sender_for_user'), # ok
    #----------------------- STATISTICS -----------------------#
    path('user/statistics/', statistics.get_statistics , name='statistics'), # ok
    #----------------------- ARTIFICIAL INTELLIGENCE -----------------------#
    path('api/search_emails_ai/', ai.search_emails_ai , name='search_emails_ai'), # ok
    path('api/search_tree_knowledge/', ai.search_tree_knowledge, name='search_tree_knowledge'), # ok
    path('api/find_user_ai/', ai.find_user_view_ai, name='find_user_view_ai'), # ok
    path('api/new_email_ai/', ai.new_email_ai, name='new_email_ai'), # ok
    path('api/correct_email_language/', ai.correct_email_language, name='correct_email_language'), # ok
    path('api/check_email_copywriting/', ai.check_email_copywriting, name='check_email_copywriting'), # ok
    path('api/generate_email_response_keywords/', ai.generate_email_response_keywords, name='generate_email_response_keywords'), # ok
    path('api/generate_email_answer/', ai.generate_email_answer, name='generate_email_answer'), # ok
    path('api/get_new_email_response/', ai.get_new_email_response, name='get_new_email_response'), # ok
    path('api/improve_draft/', ai.improve_draft, name='improve_draft'), # ok
    #----------------------- OAuth 2.0 EMAIL PROVIDERS API -----------------------#
    path('microsoft/auth_url/', auth_microsoft.generate_auth_url, name='microsoft_auth_url'), # ok
    path('microsoft/auth_url_link_email/', auth_microsoft.auth_url_link_email, name='microsoft_auth_url_link_email'), # ok
    path('microsoft/receive_mail_notifications/', webhook_microsoft.MicrosoftEmailNotification.as_view(), name='receive_mail_notifications'), # ok
    path('microsoft/receive_contact_notifications/', webhook_microsoft.MicrosoftContactNotification.as_view(), name='receive_contact_notifications'), # ok
    path('microsoft/receive_subscription_notifications/', webhook_microsoft.MicrosoftSubscriptionNotification.as_view(), name='receive_subscription_notifications'), # ok
    path('google/auth_url/', auth_google.generate_auth_url, name='google_auth_url'), # ok
    path('google/auth_url_link_email/', auth_google.auth_url_link_email, name='google_auth_url_link_email'), # ok
    path('google/receive_mail_notifications/', webhook_google.receive_mail_notifications, name='google_receive_mail_notifications'), # ok
    #----------------------- SHIPPING LABELS -----------------------#
    path('user/label_ids', search_labels.get_user_label_ids, name='get_user_label_ids'),
    path('user/labels_data', search_labels.get_labels_data, name='get_labels_data'),
    path('user/label_pdf', search_labels.get_label_pdf, name='get_label_pdf'),
    path('user/delete_labels', labels.delete_labels, name='delete_labels'),
    #----------------------- PAYMENT PROVIDER API -----------------------#
    # path('stripe/receive_payment_notifications/', views.receive_payment_notifications, name='stripe_receive_payment_notifications'), # dev
]