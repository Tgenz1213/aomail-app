from django.urls import path
from . import views

app_name = 'MailAssistant'

urlpatterns = [
    path('', views.home_page, name="home_page"),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('register/', views.register, name="register"),
    path('send_mails/', views.send_mail, name="send_mails")
    ]
