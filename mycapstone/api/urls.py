from django.urls import path
from api.views.auth_views import run_auth, create_google_calendar_event
from .views import api_views


app_name = 'api'

urlpatterns = [
    # 이벤트 생성 
    path('calendar', create_google_calendar_event, name='create_event'),
    # 메인 
    path('', api_views.apindex, name='apindex'),
    # 계정 인증 
    path('runauth/', run_auth, name='run_auth'),
]
