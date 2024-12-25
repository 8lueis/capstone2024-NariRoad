from googleapiclient.discovery import build
from django.http import HttpResponse
from django.urls import reverse
from datetime import datetime, timedelta
from ..models import Exam




import os
import pickle

# Token 및 파일 경로 설정
TOKEN_FILE = os.path.join('api', 'token.pickle')


def create_google_calendar_event(request):
    # 인증 정보 확인 및 불러오기
    if not os.path.exists(TOKEN_FILE):
        run_auth_url = reverse('api:run_auth')
        return HttpResponse(f"OAuth 인증이 필요합니다. <a href='{run_auth_url}'>여기를 클릭</a>하여 인증하세요.")

    with open(TOKEN_FILE, 'rb') as token:
        creds = pickle.load(token)

    # Google Calendar API 서비스 객체 생성
    try:
        service = build('calendar', 'v3', credentials=creds)
    except Exception as e:
        return HttpResponse(f"Google Calendar API 서비스 생성 실패: {e}")

    # Exam 데이터베이스에서 이벤트 추가
    calendar_id = "7dade858c6e59df59728ba5d2868b9bd2b9fcb1155032ecdeec740222fa52469@group.calendar.google.com"
    event_links = []  # 성공한 이벤트 링크 저장

    for index, exam in enumerate(Exam.objects.all()):
        try:
            # 시작 및 종료 시간 설정
            start_datetime = datetime.strptime(f"{exam.exam_date} {exam.start_time}", "%Y-%m-%d %H:%M").isoformat()
            end_datetime = datetime.strptime(f"{exam.exam_date} {exam.end_time}", "%Y-%m-%d %H:%M").isoformat()

            # 이벤트 본문 구성
            event_body = {
                'summary': exam.exam_name,
                'description': exam.notes,
                'start': {'dateTime': start_datetime, 'timeZone': 'Asia/Seoul'},
                'end': {'dateTime': end_datetime, 'timeZone': 'Asia/Seoul'},
                'visibility': 'public',
            }

            # 이벤트 추가
            event = service.events().insert(calendarId=calendar_id, body=event_body).execute()
            print(f"이벤트 생성 완료: {event.get('htmlLink')}")
            event_links.append(event.get('htmlLink'))

        except Exception as e:
            print(f"오류 발생 (행 {index}): {e}")

    return HttpResponse(f"Google Calendar에 이벤트가 성공적으로 추가되었습니다. 성공한 이벤트: {len(event_links)}개")

def run_auth(request):
    from api.auth import auth  # auth.py에서 인증 함수 가져오기
    auth()  # OAuth 인증 실행
    calendar_url = reverse('api:create_event')
    return HttpResponse(f"OAuth 인증이 완료되었습니다. 이제 <a href='{calendar_url}'>캘린더</a>를 이용하세요.")

