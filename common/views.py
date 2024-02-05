from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.utils import timezone
from .models import User
from .forms import UserForm
from group.models import Group, MemberState, AdminState


# Create your views here.
def main_page(request):
    if request.user.is_authenticated:
        user = request.user
        ##운영진인 모임 가져오기
        admin_groups = Group.objects.filter(admin_states__user=user)
        ##비운영진인 모임 가져오기
        member_groups = Group.objects.filter(member_states__user=user)
        ctx = {"admin_groups": admin_groups, "member_groups": member_groups}
        ##운영진 시간 계산
        admin_remaining_time = remain_time(admin_groups)
        ctx["admin_remaining_time"] = admin_remaining_time
        # 비운영진 그룹 시간계산
        member_remaining_time = remain_time(member_groups)
        ctx["member_remaining_time"] = member_remaining_time
        # 운영진인 그룹내 멤버수
        admin_group_count = member_count(admin_groups)
        ctx["admin_group_count"] = admin_group_count
        # 비운영진 그룹내 멤버수
        member_group_count = member_count(member_groups)
        ctx["member_group_count"] = member_group_count
        return render(request, "common/index.html", ctx)
    else:
        return render(request, "common/index.html")


# 남은 시간 계산 함수
def remain_time(groups):
    current_datetime = timezone.now()
    remaining_time = []
    for group in groups:
        target_datetime = group.end_date
        time_difference = target_datetime - current_datetime
        remaining_days = time_difference.days
        remaining_hours, remainder = divmod(time_difference.seconds, 3600)
        remaining_minutes, _ = divmod(remainder, 60)

        remaining_time.append({
            "group_name": group.title,
            "remaining_days": remaining_days,
            "remaining_hours": remaining_hours,
            "remaining_minutes": remaining_minutes,
        })
    return remaining_time


# 그룹별 인원수 count함수
def member_count(groups):
    member = []
    for group in groups:
        admin_state_count = AdminState.objects.filter(group=group).count()
        member_state_count = MemberState.objects.filter(group=group).count()
        member.append({
            "group_name": group.title,
            "count": admin_state_count + member_state_count,
        })
    return member


def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("common:main_page")
    else:
        form = UserForm()
    ctx = {"form": form}
    return render(request, "common/signup.html", ctx)


def logout_page(request):
    logout(request)
    return redirect("common:main_page")
