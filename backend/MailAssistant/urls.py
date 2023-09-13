from django.urls import path
from . import views
from MailAssistant import microsoft_api

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
    
    ]
