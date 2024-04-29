from django.urls import path
from . import views

urlpatterns = [
    path('emails/', views.email_list, name='email_list'),
    path('email/<str:email_id>/', views.email_detail, name='email_detail'),
    path('compose/', views.compose_email, name='compose_email'),
    path('sent/', views.sent_email, name='sent_email'), 
    path('email/<str:email_id>/reply/', views.reply_email, name='reply_email'),

    #path('emails/<str:email_id>/', views.get_email, name='get_email'),
]