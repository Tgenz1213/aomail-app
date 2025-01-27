"""
Django Rest Framework (DRF) URL Configuration for Aomail RESTful API.
"""

from django.urls import path
from aomail.email_providers.google import authentication as auth_google
from aomail.email_providers.google import webhook as webhook_google
from aomail.email_providers.microsoft import authentication as auth_microsoft
from aomail.email_providers.microsoft import webhook as webhook_microsoft
from aomail.controllers import artificial_intelligence as ai
from aomail.authentication import authentication as auth
from aomail.authentication import signup
from aomail.controllers import preferences as prefs
from aomail.controllers import (
    categories,
    filters,
    rules,
    emails,
    search_emails,
    search_api_emails,
    search_rules,
)
from aomail.controllers import statistics
from aomail.controllers import search_labels
from aomail.controllers import labels
from aomail.controllers import signatures
from aomail.payment_providers import stripe
from aomail.administration import dashboard 
from aomail.controllers import custom_categorization
from .controllers import views
from .controllers import agents

app_name = 'aomail'

urlpatterns = [
    #----------------------- AUTHENTICATION -----------------------#
    path('generate_reset_token/', auth.generate_reset_token, name='generate_reset_token'),
    path('reset_password/<str:uidb64>/<str:token>/', auth.reset_password, name='reset_password'),
    path('is_authenticated/', auth.is_authenticated, name='is_authenticated'),
    path('is_admin/', auth.is_admin, name='is_admin'),
    path('login/', auth.login, name='login'),
    path('token/refresh/', auth.refresh_token, name='refresh_token'),
    path('delete_account/', auth.delete_account, name='delete_account'),
    path('signup/', signup.signup, name='signup'),
    path('process_demo_data/', signup.process_demo_data, name='process_demo_data'),
    path('check_username/', signup.check_username, name='check_username'),
    path('user/social_api/unlink/', auth.unlink_email, name='unlink_email'),
    path('user/social_api/link/', auth.link_email, name='link_email'),
    #----------------------- CATEGORIES -----------------------#
    path('user/categories/', categories.get_user_categories, name='get_user_categories'),
    path('create_categories/', categories.create_categories, name='create_categories'),
    path('get_category_id/', categories.get_category_id, name='get_category_id'),
    path('update_category/', categories.update_category, name='update_category'),
    path('delete_category/', categories.delete_category, name='delete_category'),
    path('get_dependencies/', categories.get_dependencies, name='get_dependencies'),
    #----------------------- FILTERS -----------------------#
    path('user/filters/', filters.get_user_filter, name='get_user_filters'),
    path('create_filter/', filters.create_filter, name='create_filter'),
    path('update_filter/', filters.update_filter, name='update_filter'),
    path('delete_filter/', filters.delete_filter, name='delete_filter'),
    #----------------------- RULES -----------------------#
    path('user/rules_ids/', search_rules.get_user_rule_ids, name='get_user_rule_ids'),
    path('user/get_rules_data/', search_rules.get_rules_data, name='get_rules_data'),
    path('user/rules/<int:id_rule>/', rules.get_user_rule_by_id, name='get_user_rule_by_id'),
    path('user/delete_rules/<int:id_rule>/', rules.delete_user_rule_by_id, name='delete_user_rule_by_id'),
    path('user/create_rule/', rules.create_user_rule, name='create_user_rule'),
    path('user/update_rule/', rules.update_user_rule, name='update_user_rule'),
    path('user/emails/<int:email_id>/block_sender/', rules.set_rule_block_for_sender, name='set_rule_block_for_sender'),
    #----------------------- PREFERENCES -----------------------#
    path('user/preferences/update_username/', prefs.update_username, name='update_username'),
    path('user/preferences/update_password/', prefs.update_password, name='update_password'),
    path('user/preferences/language/', prefs.get_user_language, name='get_user_language'),
    path('user/preferences/set_language/', prefs.set_user_language, name='set_user_language'),
    path('user/preferences/theme/', prefs.get_user_theme, name='get_user_theme'),
    path('user/preferences/set_theme/', prefs.set_user_theme, name='set_user_theme'),
    path('user/preferences/timezone/', prefs.get_user_timezone, name='get_user_timezone'),
    path('user/preferences/set_timezone/', prefs.set_user_timezone, name='set_user_timezone'),
    path('user/preferences/username/', prefs.get_user_details, name='get_user_details'),
    path('user/preferences/plan/', prefs.get_user_plan, name='get_user_plan'),
    path('user/preferences/prioritization/', prefs.prioritization, name='user_prioritization'),
    #----------------------- EMAILS -----------------------#
    path('user/emails/delete_emails', emails.delete_emails, name='delete_emails'), # waiting for implementation in FE
   
    path('user/emails_ids/', search_emails.get_user_emails_ids, name='get_user_emails'),
    path('user/get_email_content/', search_emails.get_email_content, name='get_email_content'),
    path('user/get_emails_data/', search_emails.get_emails_data, name='get_emails_data'),
    path('user/get_simple_email_data/', emails.get_simple_email_data, name='get_simple_email_data'),    
    path('user/get_first_email/', emails.get_first_email, name='get_first_email'),    
    path('user/emails/update/', emails.update_emails, name='update_emails'),
    path('user/emails/<str:email_id>/attachments/<str:attachment_name>/', emails.retrieve_attachment_data, name='retrieve_attachment_data'), 
    path('get_mail_by_id', emails.get_mail_by_id, name='get_mail_by_id'),
    path('user/emails/<int:email_id>/delete/', emails.delete_email, name='delete_email'),
    path('user/emails_counts/', search_emails.get_email_counts, name='get_email_counts'),
    path('user/answer_email_suggestion_ids/', emails.get_answer_email_suggestion_ids , name='get_answer_email_suggestion_ids'),
    #----------------------- VIEWS -----------------------#
    path('pictures/<path:image_name>', views.serve_image, name='serve_image'),
    path('agent_icon/<path:image_name>', views.serve_agent_icon, name='serve_agent_icon'),
    path('user/contacts/', views.get_user_contacts, name='get_user_contacts'),
    path('user/emails_linked/', views.get_emails_linked , name='get_emails_linked'),
    path('user/get_api_emails_ids/', search_api_emails.get_api_emails_ids , name='get_api_emails_ids'),
    path('user/get_api_emails_data/', search_api_emails.get_api_emails_data , name='get_api_emails_data'),
    path('user/social_api/check_connectivity/', views.check_connectivity, name='check_connectivity'),
    path('user/social_api/synchronize/', views.synchronize, name='synchronize'),    
    path('user/social_api/send_email/', views.send_email, name='send_email'),
    path('user/social_api/send_schedule_email/', views.send_schedule_email, name='send_schedule_email'),
    path('user/social_api/get_profile_image/', views.get_profile_image, name='get_profile_image'),
    path('user/social_api/update_user_description/', views.update_user_description, name='update_user_description'),
    path('user/social_api/get_user_description/', views.get_user_description, name='get_user_description'),    
    path('create_sender', views.create_sender, name='create_sender'),
    path('check_sender', views.check_sender_for_user, name='check_sender_for_user'),
    #----------------------- STATISTICS -----------------------#
    path('user/statistics/', statistics.get_statistics , name='statistics'),
    #----------------------- ARTIFICIAL INTELLIGENCE -----------------------#
    path('user/social_api/review_user_description/', custom_categorization.review_user_description, name='review_user_description'),
    path('user/generate_categories_scratch/', custom_categorization.generate_categories_scratch, name='generate_categories_scratch'),
    path('user/generate_prioritization_scratch/', custom_categorization.generate_prioritization_scratch, name='generate_prioritization_scratch'),
    path('search_emails_ai/', ai.search_emails_ai , name='search_emails_ai'),
    path('search_tree_knowledge/', ai.search_tree_knowledge, name='search_tree_knowledge'),
    path('find_user_ai/', ai.find_user_view_ai, name='find_user_view_ai'),
    path('new_email_ai/', ai.new_email_ai, name='new_email_ai'),
    path('correct_email_language/', ai.correct_email_language, name='correct_email_language'),
    path('check_email_copywriting/', ai.check_email_copywriting, name='check_email_copywriting'),
    path('generate_email_response_keywords/', ai.generate_email_response_keywords, name='generate_email_response_keywords'),
    path('generate_email_answer/', ai.generate_email_answer, name='generate_email_answer'),
    path('get_new_email_response/', ai.get_new_email_response, name='get_new_email_response'),
    path('improve_draft/', ai.improve_draft, name='improve_draft'),
    path('handle_email_action/', ai.handle_email_action, name='handle_email_action'),
    #----------------------- OAuth 2.0 EMAIL PROVIDERS API -----------------------#
    path('microsoft/auth_url/', auth_microsoft.generate_auth_url, name='microsoft_auth_url'),
    path('microsoft/auth_url_link_email/', auth_microsoft.auth_url_link_email, name='microsoft_auth_url_link_email'),
    path('microsoft/auth_url_regrant/', auth_microsoft.auth_url_regrant, name='microsoft_auth_url_regrant'),
    path('microsoft/receive_mail_notifications/', webhook_microsoft.MicrosoftEmailNotification.as_view(), name='receive_mail_notifications'),
    path('microsoft/receive_contact_notifications/', webhook_microsoft.MicrosoftContactNotification.as_view(), name='receive_contact_notifications'),
    path('microsoft/receive_subscription_notifications/', webhook_microsoft.MicrosoftSubscriptionNotification.as_view(), name='receive_subscription_notifications'),
    path('google/auth_url/', auth_google.generate_auth_url, name='google_auth_url'),
    path('google/auth_url_link_email/', auth_google.auth_url_link_email, name='google_auth_url_link_email'),
    path('google/auth_url_regrant/', auth_google.auth_url_regrant, name='google_auth_url_regrant'), # dev
    path('google/receive_mail_notifications/', webhook_google.receive_mail_notifications, name='google_receive_mail_notifications'),
    #----------------------- SHIPPING LABELS -----------------------#
    path('user/label_ids', search_labels.get_user_label_ids, name='get_user_label_ids'),
    path('user/labels_data', search_labels.get_labels_data, name='get_labels_data'),
    path('user/label_pdf', search_labels.get_label_pdf, name='get_label_pdf'),
    path('user/delete_labels', labels.delete_labels, name='delete_labels'),
    #----------------------- ADMIN RESSOURCES -----------------------#
    path('admin/login/', dashboard.login, name='admin_login'),
    path('admin/create_superuser/', dashboard.create_superuser, name='create_superuser'),
    path('admin/update_admin_data/', dashboard.update_admin_data, name='update_admin_data'),
    path('admin/delete_admin/', dashboard.delete_admin, name='delete_admin'),    
    path('admin/get_dashboard_data/', dashboard.get_dashboard_data, name='get_dashboard_data'),
    path('admin/search_user_info/', dashboard.search_user_info, name='search_user_info'),
    path('admin/get_costs_info/', dashboard.get_costs_info, name='get_costs_info'),
    path('admin/update_user_info/', dashboard.update_user_info, name='update_user_info'),
    #----------------------- PAYMENT PROVIDER API -----------------------# 
    path('stripe/create_checkout_session/', stripe.create_checkout_session, name='stripe_create_checkout_session'), 
    path('stripe/webhook/', stripe.webhook, name='stripe_webhook'), 
    #----------------------- SIGNATURES -----------------------#
    path('user/signatures/', signatures.list_signatures, name='list_signatures'),
    path('user/signatures/create/', signatures.create_signature, name='create_signature'),
    path('user/signatures/update/', signatures.update_signature, name='update_signature'),
    path('user/signatures/<int:signature_id>/delete/', signatures.delete_signature, name='delete_signature'),
    #----------------------- AGENTS -----------------------#
    path('user/agents/', agents.list_agents, name='list_agents'),
    path('user/agents/create/', agents.create_agent, name='create_agent'),
    path('user/agents/<int:agent_id>/update/', agents.update_agent, name='update_agent'),
    path('user/agents/<int:agent_id>/delete/', agents.delete_agent, name='delete_agent'),
    path('user/agents/check_last_used/', agents.check_last_used_agent, name='check_last_used_agent'),
    path('user/agents/<int:agent_id>/', agents.get_agent, name='get_agent'),
    path('user/agents/all_info/', agents.get_all_agents_info, name='get_all_agents_info'),
]