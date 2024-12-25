from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Question(models.Model):
    TARGET_CHOICES = [
        ('TOEIC', 'TOEIC'),
        ('TOEIC4', 'TOEIC 400점대'),
        ('TOEIC5', 'TOEIC 500점대'),
        ('TOEIC6', 'TOEIC 600점대'),
        ('TOEIC7', 'TOEIC 700점대'),
        ('TOEIC8', 'TOEIC 800점대'),
        ('TOEIC9', 'TOEIC 900점대'),
        ('TOEICNEW', 'TOEIC 입문'),
        ('JLPT', 'JLPT'),
        ('JLPT5', 'JLPT N5'),
        ('JLPT4', 'JLPT N4'),
        ('JLPT3', 'JLPT N3'),
        ('JLPT2', 'JLPT N2'),
        ('JLPT1', 'JLPT N1'),
        ('JLPTNEW', 'JLPT 입문'),
        ('HSK', 'HSK'),
        ('HSK1', 'HSK 1급'),
        ('HSK2', 'HSK 2급'),
        ('HSK3', 'HSK 3급'),
        ('HSK4', 'HSK 4급'),
        ('HSK5', 'HSK 5급'),
        ('HSK6', 'HSK 6급'),
        ('HSKNEW', 'HSK 입문'),
        ('target_etc', '기타(글로 작성해 주세요.)'),
        ('nothing', '없음'),
    ]

    LANGUAGE_CHOICES = [
        ('english', '영어'),
        ('chinese', '중국어'),
        ('japanese', '일본어'),
        ('language_etc', '기타(글로 작성해 주세요.)'),
    ]

    DAY_CHOICES = [
        ('monday', '월요일'),
        ('tuesday', '화요일'),
        ('wednesday', '수요일'),
        ('thursday', '목요일'),
        ('friday', '금요일'),
        ('saturday', '토요일'),
        ('sunday', '일요일'),
        ('day_etc', '기타(글로 작성해 주세요.)')
    ]

    TIME_CHOICES = [
        ('am', '오전'),
        ('pm', '오후'),
        ('after', '수업 마친 후'),
        ('before', '수업 전'),
        ('time_etc', '기타(글로 작성해 주세요.)')
    ]
    ONLINE_CHOICES = [
        ('online', '온라인'),
        ('offline', '오프라인'),
    ]
    LOCATION_CHOICES = [
        ('library', '도서관'),
        ('cafe', '카페'),
        ('studyroom', '스터디 룸 (도서관)'),
        ('classroom', '강의실'),
        ('location_etc', '기타(글로 작성해 주세요.)'),
    ]
    CONTACT_CHOICES = [
            ('email', '이메일'),
            ('openchat', '오픈 채팅'),
            ('hywtalk', '하이유톡'),
            ('contact_etc', '기타(글로 작성해 주세요.)'),
        ]
    
    target = models.CharField(max_length=50, choices=TARGET_CHOICES, verbose_name="목표 설정", blank=True, null=True)
    desired_language = models.CharField(max_length=50, choices=LANGUAGE_CHOICES, verbose_name="희망 언어", blank=True, null=True)  
    preferred_day = models.CharField(max_length=20, choices=DAY_CHOICES, verbose_name="희망 요일",  blank=True, null=True)
    preferred_time = models.CharField(max_length=20, choices=TIME_CHOICES, verbose_name="희망 시간",  blank=True, null=True)
    online_offline = models.CharField(max_length=10, choices=ONLINE_CHOICES, verbose_name="온/오프라인",  blank=True, null=True)
    location = models.CharField(max_length=20, choices=LOCATION_CHOICES, verbose_name='희망 장소',  blank=True, null=True)
    contact_method = models.CharField(max_length=20, choices=CONTACT_CHOICES, verbose_name="연락 수단", blank=True, null=True)  
    # 캘린더 링크 받고, 연락망 받기 
    calendar_link = models.URLField(verbose_name="캘린더 링크", blank=True, null=True)
    contact_info = models.CharField(max_length=200, verbose_name="연락 정보", blank=True, null=True)

                                      
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    # author 필드는 User 모델을 ForeignKey로 적용
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # 수정 확인 속성 (수정 일시)
    modify_date = models.DateTimeField(null=True, blank=True)
    # id 값 대신 제목 조회 

    def save(self, *args, **kwargs):
        if self.pk:
            self.modify_date = now()
        super().save(*args, **kwargs)
    def __str__(self):
        return f"[{self.author}] {self.subject} ({self.create_date.strftime('%Y-%m-%d %H:%M')})"


class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # on_delete=models.CASCADE: 계정이 삭제되면 이 계정이 작성한 질문을 모두 삭제하라는 의미
    content = models.TextField()
    modify_date = models.DateTimeField(null=True, blank=True)
    create_date = models.DateTimeField()

