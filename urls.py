from django.urls import path
from . import views

app_name = 'training'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('programs/', views.programs, name='programs'),
    path('skills/', views.skills, name='skills'),
    path('settings/', views.settings, name='settings'),
]
