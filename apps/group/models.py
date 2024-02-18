from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.files.storage import FileSystemStorage
from apps.common.models import User

class Group(models.Model):
    title = models.CharField("그룹 이름", max_length=30)
    password = models.CharField("그룹 비밀번호", max_length=15)
    ability_description1 = models.CharField("실력1 설명",
                                            max_length=100,
                                            null=True,
                                            blank=True)
    ability_description2 = models.CharField("실력2 설명",
                                            max_length=100,
                                            null=True,
                                            blank=True)
    ability_description3 = models.CharField("실력3 설명",
                                            max_length=100,
                                            null=True,
                                            blank=True)
    ability_description4 = models.CharField("실력4 설명",
                                            max_length=100,
                                            null=True,
                                            blank=True)
    ability_description5 = models.CharField("실력5 설명",
                                            max_length=100,
                                            null=True,
                                            blank=True)
    # array필드를 지원하지 않기 때문에 manyToMany필드로 저장, 이 후 정보를 가져오려면 역참조하여 사용
    is_end = models.BooleanField(default=False)
    end_date = models.DateTimeField(default=timezone.now().date() +
                                    timezone.timedelta(days=3))

    def __str__(self):
        return self.title


class Idea(models.Model):
    group = models.ForeignKey(Group,
                              on_delete=models.CASCADE,
                              null=True,
                              related_name="idea_member_states")
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField("아이디어 이름", max_length=31, null=True)
    intro = models.CharField("아이디어 한 줄 소개", max_length=50, null=True)
    file = models.FileField("첨부파일",
                            upload_to="ideas/files/%Y/%m/%d/",
                            null=True,
                            blank=True)
    content = models.TextField("아이디어 설명", max_length=1000, default="자신의 아이디어를 간단하게 소개해주세요.")
    score = models.IntegerField("아이디어 점수", default=0)
    member = models.ManyToManyField(User,
                                    related_name="idea_member",
                                    blank=True)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    
class MemberState(models.Model):
    group = models.ForeignKey(Group,
                              on_delete=models.CASCADE,
                              related_name="member_states")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group_ability = models.PositiveIntegerField(
        "실력",
        validators=[MaxValueValidator(5),
                    MinValueValidator(1)],
        null=True)
    
    idea_vote1 = models.ForeignKey(Idea,
                                   on_delete=models.CASCADE,
                                   related_name="idea_vote1_set",
                                   null=True)
    idea_vote2 = models.ForeignKey(Idea,
                                   on_delete=models.CASCADE,
                                   related_name="idea_vote2_set",
                                   null=True)
    idea_vote3 = models.ForeignKey(Idea,
                                   on_delete=models.CASCADE,
                                   related_name="idea_vote3_set",
                                   null=True)
    my_team_idea = models.ForeignKey(Idea,
                                     on_delete=models.CASCADE,
                                     related_name="my_team_idea_set",
                                     null=True, blank=True)
    def __str__(self):
        return self.user.username

class AdminState(models.Model):
    group = models.ForeignKey(Group,
                              on_delete=models.CASCADE,
                              related_name="admin_states")
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Vote(models.Model):
    group = models.ForeignKey(Group,
                              on_delete=models.CASCADE,
                              related_name="votes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    idea_vote1 = models.ForeignKey(Idea,
                                   on_delete=models.CASCADE,
                                   related_name="vote1_set")
    idea_vote2 = models.ForeignKey(Idea,
                                   on_delete=models.CASCADE,
                                   related_name="vote2_set")
    idea_vote3 = models.ForeignKey(Idea,
                                   on_delete=models.CASCADE,
                                   related_name="vote3_set")

    def __str__(self):
        return f"Vote by {self.user.username} for {self.group.title}"