from django.utils import timezone
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from apps.group.models import Group
from apps.result.tasks import scheduler, current_datetime

##원하는 작업
####팀빌딩 함수 추가 하는 부분
def make_first_auto(function):
    groups = Group.objects.filter(first_end_date__gt=current_datetime)
    for group in groups:
        scheduler.add_job(function,
                          trigger=DateTrigger(group.first_end_date),
                          args=[group.id])

def make_second_auto(function):
    groups = Group.objects.filter(second_end_date__gt=current_datetime)
    for group in groups:
        scheduler.add_job(function,
                          trigger=DateTrigger(group.second_end_date),
                          args=[group.id])


# 스케줄링 작업 실행
def start_scheduler():
    scheduler.print_jobs()
    scheduler.start()


##view에서 팀빌딩 함수 실행
def first_scoring_auto(function, group):
    if group.first_end_date > current_datetime:
        scheduler.add_job(function,
                          trigger=DateTrigger(group.first_end_date),
                          args=[group.id])

def second_scoring_auto(function, group):
    if group.second_end_date > current_datetime:
        scheduler.add_job(function,
                          trigger=DateTrigger(group.second_end_date),
                          args=[group.id])

def team_building_auto(function, group):
    if group.third_end_date > current_datetime:
        scheduler.add_job(function,
                          trigger=DateTrigger(group.third_end_date),
                          args=[group.id])