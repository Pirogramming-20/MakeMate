from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.utils import timezone
from .models import User
from .forms import UserForm
from apps.group.models import Group, MemberState, AdminState, Vote


# Create your views here.
def main_page(request):
    if request.user.is_authenticated:
        user = request.user
        ##운영진인 모임 가져오기
        admin_groups = Group.objects.filter(admin_states__user=user)
        ##비운영진인 모임 가져오기
        # member_state&admin_state 둘다 존재시 admin_state를 우선으로
        member_set = set(Group.objects.filter(member_states__user=user))
        admin_set = set(admin_groups)
        member_groups = list(member_set - admin_set)
    
        ctx = {
            "admin_groups": admin_groups,
            "member_groups": member_groups,
        }
        # 운영진인 그룹내 멤버수
        admin_group_count = member_count(admin_groups)
        ctx["admin_group_count"] = admin_group_count
        # 비운영진 그룹내 멤버수
        member_group_count = member_count(member_groups)
        ctx["member_group_count"] = member_group_count
        return render(request, "common/index.html", ctx)
    else:
        return render(request, "common/index.html")


# 그룹별 인원수 count함수
def member_count(groups):
    member = []
    for group in groups:
        admin_states = set(
            AdminState.objects.filter(group=group).values_list("user",
                                                               flat=True))
        member_states = set(
            MemberState.objects.filter(group=group).values_list("user",
                                                                flat=True))
        states = admin_states.union(member_states)
        member.append({
            "group_name": group.title,
            "count": len(states),
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
