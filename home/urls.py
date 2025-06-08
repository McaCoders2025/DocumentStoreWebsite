from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.firstpage, name='firstpage'),
    path('landing_page/', views.landing_page, name='landing-page'),
    path('detail/', views.stdetails, name='detail'),
    path('studentlist/', views.studentlist, name='studentlist'),
    path('student_info/<int:pk>/', views.student_info, name='student_info'),
    path('student_score/<int:pk>/', views.student_score, name='student_score'),
    path('login/', views.login_page, name='login_page'),
    path('register/', views.register, name='register'),
    path('marksheet/<str:email>/', views.student_marksheet, name='student_marksheet'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    #path('send-email/', views.send_email_to_student, name="send-email"),
    path('download/<rollnumber>/', views.download_marksheet, name='download_marksheet'),
    path('send-email/<int:rollnumber>/', views.send_email_to_student, name='send_email_to_student'),
    
]
