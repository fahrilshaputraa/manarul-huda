from django.urls import path
from . import views

app_name = 'blogpages'

urlpatterns = [
    path('clap/<int:blog_id>/', views.add_clap, name='add_clap'),
]
