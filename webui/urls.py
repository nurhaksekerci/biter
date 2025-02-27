from django.urls import path
from . import views

app_name = 'webui'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('attorney/', views.attorney, name='attorney'),
    path('attorney-details/<int:id>/', views.attorney_details, name='attorney_details'),
    path('practice/', views.practice, name='practice'),
    path('practice-details/<int:id>/', views.practice_details, name='practice_details'),
    path('case-study/', views.case_study, name='case_study'),
    path('case-study-details/<int:id>/', views.case_study_details, name='case_study_details'),
    path('blog/', views.blog, name='blog'),
    path('blog-details/<int:id>/', views.blog_details, name='blog_details'),
    path('contact/', views.contact, name='contact'),
    path('appointment/', views.appointment, name='appointment'),
    path('privacy-policy/', views.privacy_policy, name='privacy'),
    path('terms-conditions/', views.terms_conditions, name='terms_conditions'),
    path('coming-soon/', views.not_found, name='not_found'),
] 