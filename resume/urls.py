from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', auth_views.LoginView.as_view(), name='login'), 
    path('home/', views.home, name='home'), # The default route will show the login page
    path('job-preference/', views.job_preference, name='job_preference'),
    path('resumes/', views.resume_list, name='resume_list'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('feedback/<int:resume_id>/', views.feedback, name='feedback'), 
    path('jobs/', views.job_list, name='job_list'), # New URL for feedback
    path('generate-pdf/<int:resume_id>/', views.generate_pdf_resume, name='generate_pdf_resume'),
]
