from google_auth_oauthlib.flow import InstalledAppFlow
import os 
import pickle 
from django.conf import settings




SCOPES = ['https://www.googleapis.com/auth/calendar']
creds_filename = os.path.join(settings.BASE_DIR, 'api', 'credentials.json')  # 파일 위치에 따라 수정 필요'credentials.json'
token_file = os.path.join(settings.BASE_DIR, 'api', 'token.pickle')  


def auth():
    creds = None
    # 기존 인증 정보가 있으면 불러오기 
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(creds_filename, SCOPES)
        creds = flow.run_local_server(port=8080) # prompt='consent' : refresh_token이 항상 생성되도록 설정

        # 인증 정보를 파일에 저장 
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)
    return creds 

