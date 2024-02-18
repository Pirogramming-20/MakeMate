import json
import mimetypes
from enum import Enum
import numpy as np
from urllib.parse import parse_qs
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, FileResponse, HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from apps.common.models import User
from apps.group.models import Group, MemberState, AdminState, Idea, Vote
from apps.group.views import State, TeamNumber, redirect_by_auth
from apps.groupSetting.forms import NonAdminInfoForm
from .tasks import team_building_auto, start_scheduler, make_auto


# Create your views here.
@login_required(login_url="common:login")
def result(request, group_id):  # 최종 결과 페이지
    group = Group.objects.get(id=group_id)
    idea_list = Idea.objects.filter(group=group).order_by("-score")[:5]
    members = MemberState.objects.filter(group=group)
    state = redirect_by_auth(request.user, group_id)

    group.is_second_end = True
    group.save()

    current_time = timezone.now()
    if current_time >= group.third_end_date and group.is_third_end:
        if state == State.WITH_HISTORY or state == State.ADMIN:
            ctx = {"idea_list": idea_list, "members": members, "group": group}
            return render(request, "group/result.html", context=ctx)
        else:
            return redirect("/")
    else:
        redirect_url = reverse("group:group_detail",
                               kwargs={"group_id": group_id})
        return redirect(redirect_url)


def calculate_members_ability(members):
    members_ability = []

    for member in members:
        members_ability.append(member.group_ability)
    return members_ability


def calculate_project_average_ability(idea_list):
    project_average_ability = []

    for idea in idea_list:
        followers = MemberState.objects.filter(user__in=idea.member.all())
        score = 0

        for follower in followers:
            score += follower.group_ability

        score = score / (len(followers))

        project_average_ability.append(score)

    project_average_ability.sort()
    return project_average_ability


def calculate_project_pick(members, idea_list):
    project_pick = np.zeros(
        (len(idea_list), len(members)))  # 각 인원 별로 지망도를 2차원 배열로 만들거임.

    for member_idx, member in enumerate(members):
        for project_idx, project in enumerate(idea_list):
            if project == member.idea_vote1:
                project_pick[project_idx][member_idx] = 4
            elif project == member.idea_vote2:
                project_pick[project_idx][member_idx] = 3
            elif project == member.idea_vote3:
                project_pick[project_idx][member_idx] = 2
            else:
                project_pick[project_idx][member_idx] = 1
    return project_pick


# 리더 설정 보조함수
def selected_idea_leader(idea_list, group):
    for idea in idea_list:
        idea.member.add(idea.author)
        leader_state = MemberState.objects.get(group=group, user=idea.author)
        leader_state.my_team_idea = idea
        leader_state.save()


# idea copy함수
def idea_copy(idea_list):
    idea_titles = []
    for idea in idea_list:
        idea_titles.append(idea.title)
    return idea_titles


# 멤버 copy함수
def member_copy(members):
    member_name = []
    for member in members:
        member_name.append(member.user.username)
    return member_name


# 원본데이터로 변환 함수
def idea_change(idea_titles, group):
    idea_list = []
    for idea in idea_titles:
        idea_list.append(Idea.objects.get(title=idea, group=group))
    return idea_list


# 원본데이터로 변환 함수
def members_change(members_name):
    members = []
    for member in members_name:
        members.append(
            MemberState.objects.filter(user__username=member).first())
    return members


def start_team_building(group_id):
    group = Group.objects.get(id=group_id)
    idea_list = Idea.objects.filter(
        group=group).order_by("-score")[:TeamNumber.THIRD_TEAM.value]

    ##members에서 팀장들은 뺼필요가 있음(exclude로 빈값이 아닌것은 제외)
    selected_idea_leader(idea_list, group)
    members = MemberState.objects.filter(
        group=group,
        group_ability__isnull=False).exclude(my_team_idea__isnull=False)

    if len(members) == 0:
        pass
    else:
        project_average_ability = []
        # 나중에 "project_pick"을 만들 때 필요함. 사이클 한번당 수정이 필요함.
        # 나중에 "project_pick"을 만들 때 필요함.
        members_ability = (
            []
        )  # 후에 project_average_ability와 meshigrid하여 서로 뺄 거임. 사이클 한번당 수정이 필요함.

        members_ability = calculate_members_ability(
            members)  # member_ability 리스트에 그룹 내 모든 멤버의 실력을 저장하는 코드.

        project_average_ability = calculate_project_average_ability(
            idea_list)  # 각 아이디어 별로 평균 실력을 리스트로 저장하는 코드.

        members_ability, project_average_ability = np.meshgrid(
            members_ability,
            project_average_ability)  # 위의 두 리스트를 2차원 배열로 만들어 빼줄거임.

        project_pick = calculate_project_pick(members, idea_list)

        project_fitness = np.transpose(
            abs(members_ability - project_average_ability) + project_pick)

        make_team(idea_list, members, project_fitness,
                  group_id)  # 임시로 홈으로 리디렉션 되도록 설정함.
    return redirect("/")


def team_building_cycle(group_id, members):
    if len(members) == 0:
        pass
    else:
        group = Group.objects.get(id=group_id)
        idea_list = Idea.objects.filter(
            group=group).order_by("-score")[:TeamNumber.THIRD_TEAM.value]
        project_average_ability = [
        ]  # 나중에 "project_pick"을 만들 때 필요함. 사이클 한번당 수정이 필요함.
        members_ability = (
            []
        )  # 후에 project_average_ability와 meshigrid하여 서로 뺄 거임. 사이클 한번당 수정이 필요함.

        members_ability = calculate_members_ability(
            members)  # member_ability 리스트에 그룹 내 모든 멤버의 실력을 저장하는 코드.

        project_average_ability = calculate_project_average_ability(
            idea_list)  # 각 아이디어 별로 평균 실력을 리스트로 저장하는 코드.

        members_ability, project_average_ability = np.meshgrid(
            members_ability,
            project_average_ability)  # 위의 두 리스트를 2차원 배열로 만들어 빼줄거임.

        project_pick = calculate_project_pick(members, idea_list)

        project_fitness = np.transpose(
            abs(members_ability - project_average_ability) + project_pick)

        return idea_list, members, project_fitness


def make_team(idea_list, members, project_fitness, group_id):
    group = Group.objects.get(id=group_id)
    # 사본 만들기
    idea_titles = idea_copy(idea_list)
    members_name = member_copy(members)
    if len(idea_titles) > 0:
        # 각열에서 가장 큰숫자의 인덱스 찾기
        argmax_columns = np.argmax(project_fitness, axis=0).astype(int)
        # 조건에 만족하는 팀&member 좌표 찾기
        selected_column = int(
            np.argmin(
                project_fitness[argmax_columns.astype(int),
                                range(project_fitness.shape[1])]).astype(int))
        selected_row = int(argmax_columns[selected_column])
        # arrary_update
        project_fitness = np.delete(project_fitness, selected_row, axis=0)
        project_fitness = np.delete(project_fitness, selected_column, axis=1)
        # 해당 그룹에 member 추가
        idea_list[selected_column].member.add(members[selected_row].user)
        members[selected_row].my_team_idea = idea_list[selected_column]
        members[selected_row].save()
        # 추가된 인원&팀 삭제
        del members_name[selected_row]
        del idea_titles[selected_column]

        if len(members_name) == 0:
            return redirect("/")
        else:
            idea_list = idea_change(idea_titles, group)
            members = members_change(members_name)
            make_team(idea_list, members, project_fitness, group_id)
    else:
        if len(members) > 0:
            up_idea_list, up_members, up_project_fitness = team_building_cycle(
                group_id, members)
            make_team(up_idea_list, up_members, up_project_fitness, group_id)


""" # ##스케줄러 시작##
make_auto(start_team_building)
start_scheduler()
# #### """
