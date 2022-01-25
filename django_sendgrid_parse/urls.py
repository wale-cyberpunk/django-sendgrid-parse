from django.urls import path

from . import views

app_name = 'django_sendgrid_parse'
urlpatterns = [
    path('', views.sendgrid_email_receiver, name='webhook'),
]
