from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from common.models import User

class Group(models.Model):
    STACK_POSITION = (
        ("PM", "기획"),
        ("DESIGN", "디자인"),
        ("FE", "프론트엔드"),
        ("BE", "백엔드"),
        ("SERVER", "배포/서버"),
    )
    TYPE_CHOICE = (
        ("모각코", "모각코"),
        ("프로젝트", "프로젝트"),
    )
    title = models.CharField("그룹 이름", max_length=30)
    team_number = models.PositiveIntegerField(
        "그룹 내 팀 수",
        default=1,
        validators=[MaxValueValidator(10), MinValueValidator(1)])
    password = models.CharField("그룹 비밀번호", max_length=15)
    type = models.CharField("모임 종류", max_length=20, choices=TYPE_CHOICE)
    ability_description1 = models.CharField("실력1 설명", max_length=100, null=True, blank=True)
    ability_description2 = models.CharField("실력2 설명", max_length=100, null=True, blank=True)
    ability_description3 = models.CharField("실력3 설명", max_length=100, null=True, blank=True)
    ability_description4 = models.CharField("실력4 설명", max_length=100, null=True, blank=True)
    ability_description5 = models.CharField("실력5 설명", max_length=100, null=True, blank=True)
    choice = models.IntegerField("그룹 최대 투표 개수", default=3, null=True)
    tech_stack = models.CharField("기술 스택", max_length=10, choices=STACK_POSITION)
    # array필드를 지원하지 않기 때문에 manyToMany필드로 저장, 이 후 정보를 가져오려면 역참조하여 사용
    # team_building = models.ManyToManyField(User, related_name='user_groups', null=True)
    end_date = models.DateTimeField(default=timezone.now().date() + timezone.timedelta(days=3))
    
    def __str__(self):
        return self.title
    
class Idea(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, related_name="idea_member_states")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField("아이디어 이름", max_length=31, null=True)
    intro = models.CharField("아이디어 한 줄 소개", max_length=50, null=True)
    file = models.FileField("아이디어 파일", blank=True, upload_to='idea/%Y%m%d')
    content = models.TextField("아이디어 설명", max_length=1000, default="기본 설명")
    score = models.IntegerField("아이디어 점수", default=0)
    member = models.ManyToManyField(User, related_name='idea_member', blank=True)

    def __str__(self):
        return self.title
    
class MemberState(models.Model):
    STACK_POSITION = (
        ("PM", "기획"),
        ("DESIGN", "디자인"),
        ("FE", "프론트엔드"),
        ("BE", "백엔드"),
        ("SERVER", "배포/서버"),
    )
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="member_states")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group_ability = models.PositiveIntegerField("실력", validators=[MaxValueValidator(5), MinValueValidator(1)], null=True)
    group_tech_stack = models.CharField("기술 스택", max_length=10, choices=STACK_POSITION, null=True)
    idea_vote1 = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name="idea_vote1_set", null=True)
    idea_vote2 = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name="idea_vote2_set", null=True)
    idea_vote3 = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name="idea_vote3_set", null=True)

class AdminState(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="admin_states")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
