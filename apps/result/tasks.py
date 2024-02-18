from django.utils import timezone
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from apps.group.models import Group

scheduler = BackgroundScheduler()

current_datetime = timezone.now()


##원하는 작업
####팀빌딩 함수 추가 하는 부분
def make_third_auto(function):
    groups = Group.objects.filter(third_end_date__gt=current_datetime)
    for group in groups:
        scheduler.add_job(function,
                          trigger=DateTrigger(group.third_end_date),
                          args=[group.id])


# 스케줄링 작업 실행
def start_scheduler():
    scheduler.print_jobs()
    scheduler.start()


##view에서 팀빌딩 함수 실행
def team_building_auto(function, group):
    if group.third_end_date > current_datetime:
        scheduler.add_job(function,
                          trigger=DateTrigger(group.third_end_date),
                          args=[group.id])
