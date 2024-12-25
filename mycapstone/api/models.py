from django.db import models


class Exam(models.Model):
    # Django는 테이블 이름을 자동으로 'app명_클래스명' 형태로 생성합니다.
    # 원하는 이름을 사용하려면 Meta 클래스에서 지정합니다.

    exam_name = models.CharField(max_length=50, null=False)  # 문자열 필드
    exam_date = models.DateField(null=False)  # 날짜 필드
    start_time = models.CharField(max_length=10, null=False)  # 문자열 필드
    end_time = models.CharField(max_length=10, null=False)  # 문자열 필드
    notes = models.TextField(null=True, blank=True)  # 텍스트 필드 (nullable)

    class Meta:
        db_table = 'exam'  # 테이블 이름 명시

    def __str__(self):
        return f'{self.exam_name} - {self.exam_date}'
