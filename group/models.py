from django.db import models
from common.models import User
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

stack_position = (
        ('PM', '기획'),
        ('DESIGN', '디자인'),
        ('FE', '프론트엔드'),
        ('BE', '백엔드'),
        ('SERVER', '배포/서버'),
    )

type_choice = (
        ('모각코', '모각코'),
        ('프로젝트', '프로젝트'),
    )

class Group(models.Model):
    title = models.CharField('그룹 이름', max_length=30)
    team_number = models.PositiveIntegerField('그룹 내 팀 수', validators=[MaxValueValidator(10), MinValueValidator(1)])
    password = models.CharField('그룹 비밀번호', max_length=15)
    type = models.CharField('모임 종류', max_length=20, choices=type_choice)
    ability_description1 = models.CharField('실력1 설명', max_length=100, null=True)
    ability_description2 = models.CharField('실력2 설명', max_length=100, null=True)
    ability_description3 = models.CharField('실력3 설명', max_length=100, null=True)
    ability_description4 = models.CharField('실력4 설명', max_length=100, null=True)
    ability_description5 = models.CharField('실력5 설명', max_length=100, null=True)
    choice = models.IntegerField('그룹 최대 투표 개수', default=3, null=True)
    tech_stack = models.CharField('기술 스택', max_length=10, choices=stack_position)
    #array필드를 지원하지 않기 때문에 manyToMany필드로 저장, 이 후 정보를 가져오려면 역참조하여 사용
    team_building = models.ManyToManyField(User, related_name='user_groups', null=True)
    end_date = models.DateField()

    #3일 뒤로 end_date필드가 저장 되어야하므로 내장 함수를 통해 처리
    def save(self, *args, **kwargs):
        # 객체가 처음 생성되는 경우에만 설정
        if not self.end_date:
            self.end_date = timezone.now().date() + timezone.timedelta(days=3)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title