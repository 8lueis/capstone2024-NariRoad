from django.shortcuts import render, HttpResponse
import pickle
import os
from datetime import datetime, timedelta
from googleapiclient.discovery import build



TOKEN_FILE = os.path.join('api', 'token.pickle')


def apindex(request):
    calendar_url  = "https://calendar.google.com/calendar/embed?src=7dade858c6e59df59728ba5d2868b9bd2b9fcb1155032ecdeec740222fa52469%40group.calendar.google.com&ctz=Asia%2FSeoul"
    

    if not os.path.exists(TOKEN_FILE):
        return HttpResponse("OAuth 인증이 필요합니다.")

    with open(TOKEN_FILE, 'rb') as token:
        creds = pickle.load(token)

    # 이벤트 리스트를 가져오기 위한 로직 추가
    try:
        service = build('calendar', 'v3', credentials=creds)
        timeMin = datetime.now().isoformat() + 'Z'
        timeMax = (datetime.now() + timedelta(days=90)).isoformat() + 'Z'

        calendar_id = "7dade858c6e59df59728ba5d2868b9bd2b9fcb1155032ecdeec740222fa52469@group.calendar.google.com"

        # 이벤트 가져오기
        events_result = service.events().list(
            calendarId=calendar_id,
            timeMin=timeMin,
            timeMax=timeMax,
            singleEvents=True,
            orderBy='startTime',
            maxResults=4  # 최대 4개만 가져옴
        ).execute()

        events = events_result.get('items', [])
        event_details = []

        filter_date = datetime.now()  # 오늘 날짜와 시간

        for event in events:
            summary = event.get('summary', '제목 없음')
            start_time = event['start'].get('dateTime', event['start'].get('date'))
             # 시작 시간 포맷 변경 (YYYY년 MM월 DD일)
            if start_time:
                event_datetime = datetime.fromisoformat(start_time[:19])
                # 이전 일정 X 
                if event_datetime >= filter_date:
                    # -년 -월 - 일로 출력 
                    formatted_date = event_datetime.strftime("%Y년 %m월 %d일")
                    event_details.append({
                        'summary': summary,
                        'start_time': formatted_date,  # 포맷된 날짜 전달
                        'html_link': event.get('htmlLink')
                    })

        # 템플릿에 데이터 전달
        context = {
            'calendar_url': calendar_url,  # 기존 역할 유지
            'events': event_details        # 추가된 이벤트 리스트
        }
        return render(request, 'api/calendar.html', context)

    except Exception as e:
        # 오류 발생 시 기존 캘린더만 표시
        return render(request, 'api/calendar.html', {
            'calendar_url': calendar_url,
            'error': f"이벤트를 가져오는 중 오류가 발생했습니다: {e}"
        })
