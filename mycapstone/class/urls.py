from django.urls import path
from . import views

app_name = 'class'

urlpatterns = [
    path('schedule/', views.schedule_table, name='schedule_table'),
]
