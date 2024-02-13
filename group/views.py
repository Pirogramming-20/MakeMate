import json
import mimetypes
from enum import Enum
import numpy as np
from urllib.parse import parse_qs
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, FileResponse
from django.utils import timezone
from django.urls import reverse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from common.models import User
from .models import Group, MemberState, AdminState, Idea, Vote
from .forms import *


# 유저 상태를 저장하는 ENUM
class State(Enum):
    NO_HISTORY = 0
    WITH_HISTORY = 1
    ADMIN = 2


# Create your views here.
@login_required(login_url="common:login")
def check_nonadmin(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    state = redirect_by_auth(request.user, group_id)  # 권한에 따른 리다이렉트
    wrong_flag = False  # 비밀번호가 틀리면 화면에 에러 렌더링

    if state == State.WITH_HISTORY:  # 이전 인증 내역이 있는 참여자
        return redirect(f"/group/{group_id}/")

    elif state == State.ADMIN:  # 운영진인 경우
        return redirect(f"/group/{group_id}/admin/")

    if request.method == "POST":
        form = GroupPasswordForm(request.POST)
        if form.is_valid():
            password_form = form.save(commit=False)

            if group.password == password_form.password:  # 비밀번호가 일치했을 때
                new_state = MemberState()
                new_state.group = group
                new_state.user = request.user
                new_state.save()
                return redirect(f"/group/{group_id}/non_admin_info/")
            else:
                wrong_flag = True
    form = GroupPasswordForm()
    ctx = {"group": group, "is_wrong": wrong_flag, "form": form}
    return render(request, "group/group_nonadmin_certification.html", ctx)


@login_required(login_url="common:login")
def check_admin(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    state = redirect_by_auth(request.user, group_id)  # 권한에 따른 리다이렉트
    wrong_flag = False  # 비밀번호가 틀리면 화면에 에러 렌더링

    if state == State.WITH_HISTORY:
        return redirect(f"/group/{group_id}/")

    elif state == State.ADMIN:
        return redirect(f"/group/{group_id}/admin")

    if request.method == "POST":
        form = GroupPasswordForm(request.POST)
        if form.is_valid():
            password_form = form.save(commit=False)
            if group.password == password_form.password:  # 비밀번호가 일치했을 때
                new_state = AdminState()
                new_state.group = group
                new_state.user = request.user
                new_state.save()
                return redirect(f"/group/{group_id}/admin/")
            else:
                wrong_flag = True
    form = GroupPasswordForm()
    ctx = {"group": group, "is_wrong": wrong_flag, "form": form}
    return render(request, "group/group_admin_certification.html", ctx)


def info_nonadmin(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    state = redirect_by_auth(request.user, group_id)  # 권한에 따른 리다이렉트
    user_state = MemberState.objects.filter(user=request.user,
                                            group_id=group_id).first()

    if state == State.ADMIN:  # 운영진인 경우
        return redirect(f"/group/{group_id}/admin/")

    if request.method == "POST":
        form = NonAdminInfoForm(request.POST, instance=user_state)
        if form.is_valid():
            form.save()
            return redirect(f"/group/{group_id}/")

    form = NonAdminInfoForm()
    ctx = {"group": group, "form": form}
    return render(request, "group/group_member_info.html", ctx)


def redirect_by_auth(user, group_id):
    user_state = MemberState.objects.filter(user=user,
                                            group_id=group_id).first()

    admin_state = AdminState.objects.filter(user=user,
                                            group_id=group_id).first()

    if user_state:
        if user_state.group is None:
            return State.NO_HISTORY
        else:
            return State.WITH_HISTORY

    if admin_state:
        return State.ADMIN

    return State.NO_HISTORY


# 모임 개설 메인 함수
def group_base_info(request):
    if request.method == "POST":
        # request를 딕셔너리 형태로 변환 및 state 확인
        request_dict = parse_qs(request.body.decode("utf-8"))
        data_query = request_dict["cur_data"][0]
        data_dict = parse_qs(data_query)
        req = {key: values[0] for key, values in data_dict.items()}

        # 이전 form 작성 정보가 있을 경우 prev_req로 저장
        if "prev_data" in request_dict:
            prev_data_query = parse_qs(
                request.body.decode("utf-8"))["prev_data"][0]
            prev_data_dict = parse_qs(prev_data_query)
            prev_req = {
                key: values[0]
                for key, values in prev_data_dict.items()
            }

        state = int(req["state"])  # 현재 step 정보 저장

        if state == 0:
            form = GroupBaseForm(data=req)
            return handle_form_valid(form, state, req)

        elif state == 1:
            form = GroupDetailForm(data=req)
            return handle_form_valid(form, state, req, prev_req)

        elif state == 2:
            form = GroupDateForm(data=req)
            return handle_form_valid(form, state, req, prev_req, request.user)

    form = GroupBaseForm()
    ctx = {"form": form, "state": 0}
    return render(request, "setting/setting_basic.html", context=ctx)


# 모임 개설 헬퍼 함수
# form이 유효할 때 알맞은 JSON 데이터를 return
def handle_form_valid(form, state, req, prev_req=None, user=None):
    if form.is_valid():
        if state == 0 or state == 1:
            ctx = get_context_data(form, req, prev_req, state)
            return JsonResponse(ctx)

        if state == 2:  # 마지막 단계
            prev_req = get_prev_data(form, prev_req, req, state)
            group = save_group_data(prev_req, user)
            ctx = {"state": state, "is_valid": True, "group_id": group.id}
            return JsonResponse(ctx)

    else:  # non field 또는 field 에러 전송
        ctx = {
            "state": state,
            "is_valid": False,
            "errors": form.errors,
            "non_field_errors": form.non_field_errors(),
        }
        return JsonResponse(ctx)


# 모임 개설 헬퍼 함수
def get_context_data(form, req, prev_req, state):
    form_html = get_form_html(state)
    prev_data = get_prev_data(form, prev_req, req, state)
    ctx = {
        "form_html": form_html,
        "is_valid": True,
        "state": state,
        "prev_data": prev_data,
    }
    return ctx


# 모임 개설 헬퍼 함수
def get_form_html(state):
    if state == 0:
        return GroupDetailForm().as_p()
    else:
        return GroupDateForm().as_p()


# 모임 개설 헬퍼 함수
# req 데이터에서 prev_data를 추출하여 리턴
def get_prev_data(form, prev_req, req, state):
    if state == 0:
        prev_req = {
            "title": req["title"],
            "team_number": req["team_number"],
            "password": req["password"],
            "type": req["type"],
        }

    if state == 1:
        for idx in range(1, 6):
            prev_req[f"group_ability{idx}"] = req.get(
                f"ability_description{idx}", "")

        prev_req["choice"] = int(req["choice"])

    if state == 2:
        prev_req["end_date"] = form.cleaned_data["end_date"]

    return prev_req


# 모임 개설 헬퍼 함수
# 마지막 단계에 group 데이터 저장
def save_group_data(prev_req, user):
    group = Group.objects.create(
        title=prev_req["title"],
        team_number=int(prev_req["team_number"]),
        password=prev_req["password"],
        type=prev_req["type"],
        ability_description1=prev_req.get("group_ability1", ""),
        ability_description2=prev_req.get("group_ability2", ""),
        ability_description3=prev_req.get("group_ability3", ""),
        ability_description4=prev_req.get("group_ability4", ""),
        ability_description5=prev_req.get("group_ability5", ""),
        choice=int(prev_req["choice"]),
        end_date=prev_req["end_date"],
    )

    AdminState.objects.create(group=group, user=user)

    return group


def group_share(request, group_id):
    group = Group.objects.get(id=group_id)
    ctx = {"group": group}
    return render(request, "setting/setting_sharing.html", context=ctx)


def preresult(request, group_id):
    # 그룹에 있는 아이디어를 모두 가져오고, 이를 투표점수 순서로 정렬
    # 그리고 동점자 처리도 해야하는데 그건 추후 다같이 결정
    group = Group.objects.get(id=group_id)
    idea_list = Idea.objects.filter(
        group=group).order_by("-score")[:group.team_number]
    members = MemberState.objects.filter(group=group)
    state = redirect_by_auth(request.user, group_id)

    ctx = {"idea_list": idea_list, "members": members, "group": group}
    return render(request, "preresult/preresult_admin.html", context=ctx)


def admin_page(request, group_id):
    group_instance = get_object_or_404(Group, id=group_id)
    # 운영진 인원
    admin_states_users = list(group_people(group_instance, "admin"))
    # 멤버 인원
    raw_member_states_users = list(group_people(group_instance, "member"))
    # 겹치는 인원뺴주기
    admin_set = set(admin_states_users)
    member_set = set(raw_member_states_users)
    member_states_users = list(member_set - admin_set)
    ctx = {
        "group_instance": group_instance,
        "admin_states_users": admin_states_users,
        "member_states_users": member_states_users,
    }
    return render(request, "admin/group_admin.html", ctx)


# 운영진&비운영진 멤버 리스트뽑는 함수
def group_people(group_instance, state):
    if state == "admin":
        users_ids = group_instance.admin_states.values_list("user", flat=True)
    elif state == "member":
        users_ids = group_instance.member_states.values_list("user", flat=True)

    users = User.objects.filter(id__in=users_ids)
    return users


def group_user_delete(request, group_id, user_id):
    if request.method == "POST":
        if AdminState.objects.filter(user__id=user_id,
                                     group__id=group_id).exists():
            admin_user_state = get_object_or_404(AdminState,
                                                 user__id=user_id,
                                                 group__id=group_id)
            admin_user_state.delete()
            member_user_state = get_object_or_404(MemberState,
                                                  user__id=user_id,
                                                  group__id=group_id)
            member_idea = Idea.objects.filter(author__id=user_id,
                                              group__id=group_id)
            member_idea.delete()
            member_user_state.delete()
        elif MemberState.objects.filter(user__id=user_id,
                                        group__id=group_id).exists():
            member_user_state = get_object_or_404(MemberState,
                                                  user__id=user_id,
                                                  group__id=group_id)
            member_idea = Idea.objects.filter(author__id=user_id,
                                              group__id=group_id)
            member_idea.delete()
            member_user_state.delete()
        return redirect("group:admin_page", group_id=group_id)


# patch말고 일단 POST
def group_user_update(request, group_id, user_id):
    group = get_object_or_404(Group, id=group_id)
    if request.method == "GET":
        user = User.objects.get(id=user_id)
        user_state = MemberState.objects.get(user=user, group=group)
        form = NonAdminInfoForm(instance=user_state)
        ctx = {
            "form": form,
            "group": group,
            "user_state": user_state,
            "user": user
        }
        return render(request, "admin/group_admin_modify.html", ctx)
    elif request.method == "POST":
        user_state = MemberState.objects.get(user_id=user_id)
        form = NonAdminInfoForm(request.POST, instance=user_state)
        if form.is_valid():
            form.save()
        return redirect("group:admin_page", group_id=group_id)


##Admin state 추가
@csrf_exempt
def admin_add(request, group_id):
    user_data = json.loads(request.body)
    user = User.objects.get(id=user_data["user_id"])
    group = Group.objects.get(id=user_data["group_id"])
    # Admin_state생성
    new_admin = AdminState.objects.create(user=user, group=group)
    return JsonResponse({"group_id": group_id})


##Admin state제거
@csrf_exempt
def admin_delete(request, group_id):
    user_data = json.loads(request.body)
    user = User.objects.get(id=user_data["user_id"])
    group = Group.objects.get(id=user_data["group_id"])
    # Admin_state 삭제
    bye_admin = get_object_or_404(AdminState, user=user, group=group)
    bye_admin.delete()
    return JsonResponse({"message": "AdminState deleted successfully"})


def preresult_modify(request, group_id):
    group = Group.objects.get(id=group_id)
    idea_list = Idea.objects.filter(
        group=group).order_by("-score")[:group.team_number]
    members = MemberState.objects.filter(group=group)

    if request.method == "POST":
        selected_values = request.POST.get("team_modify").split(",")
        member_id = int(selected_values[0])
        idea_id = int(selected_values[1])
        mod_mem = MemberState.objects.get(id=member_id)
        prev_idea = mod_mem.my_team_idea
        mod_idea = Idea.objects.get(id=idea_id)

        # (전제)팀장은 수정 페이지에서 팀 변경되면 안됨. 함수 실행X 바로 리디렉션
        for idea in idea_list:
            if idea.author == mod_mem.user:
                url = reverse("group:preresult", args=[group.id])
                return redirect(url)

        # (수정과정1)전에 있던 아이디어의 멤버에서 해당 멤버스테이트의 유저를 지움(수정한 아이디어의 멤버를 추가하기 위해서)
        if prev_idea != mod_idea:
            prev_idea.member.remove(mod_mem.user)
            prev_idea.save()
        # (수정과정2)해당 멤버스테이트의 최종 팀을 수정한 아이디어의 팀으로 설정
        mod_mem.my_team_idea = mod_idea
        mod_mem.save()
        # (수정과정3)수정한 아이디어의 멤버에 해당 멤버스테이트의 유저를 추가.
        mod_idea.member.add(mod_mem.user)
        mod_idea.save()

        url = reverse("group:preresult", args=[group.id])
        return redirect(url)
    else:
        ctx = {
            "members": members,
            "idea_list": idea_list,
            "group": group,
        }
        return render(request, "preresult/preresult_modify.html", context=ctx)


def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    author_ideas = Idea.objects.filter(group=group, author=request.user)
    other_ideas = Idea.objects.filter(group=group).exclude(author=request.user)
    user_state = MemberState.objects.filter(user=request.user,
                                            group=group).first()

    ideas_votes = {}
    if user_state:
        ideas_votes["idea_vote1_id"] = user_state.idea_vote1_id
        ideas_votes["idea_vote2_id"] = user_state.idea_vote2_id
        ideas_votes["idea_vote3_id"] = user_state.idea_vote3_id

    has_voted = user_state and (user_state.idea_vote1 or user_state.idea_vote2
                                or user_state.idea_vote3)

    ctx = {
        "group": group,
        "author_ideas": author_ideas,
        "other_ideas": other_ideas,
        "ideas_votes": ideas_votes,
        "has_voted": has_voted,
    }
    return render(request, "group/group_detail.html", ctx)


def idea_create(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    if Idea.objects.filter(group=group, author=request.user).exists():
        messages.error(request, "이미 이 그룹에 대한 아이디어를 제출했습니다.")
        return redirect("group:group_detail", group_id=group.id)

    if request.method == "POST":
        form = IdeaForm(request.POST, request.FILES)
        if form.is_valid():
            idea = form.save(commit=False)
            idea.group = group
            idea.author = request.user
            idea.save()
            return redirect("group:group_detail", group_id=group.id)
    else:
        form = IdeaForm()
    ctx = {
        "form": form,
        "group": group,
    }
    return render(request, "group/group_idea_create.html", ctx)


def idea_modify(request, group_id, idea_id):
    group = get_object_or_404(Group, id=group_id)
    idea = get_object_or_404(Idea,
                             id=idea_id,
                             group=group,
                             author=request.user)

    if request.method == "POST":
        form = IdeaForm(request.POST, request.FILES, instance=idea)
        if form.is_valid():
            form.save()
            return redirect("group:idea_detail",
                            group_id=group.id,
                            idea_id=idea.id)
    else:
        form = IdeaForm(instance=idea)

    ctx = {
        "form": form,
        "group": group,
        "idea": idea,
    }
    return render(request, "group/group_idea_modify.html", ctx)


def idea_delete(request, group_id, idea_id):
    group = get_object_or_404(Group, id=group_id)
    idea = get_object_or_404(Idea,
                             id=idea_id,
                             group=group,
                             author=request.user)

    if request.method == "POST" and request.POST.get("action") == "delete":
        idea.delete()
        return redirect("group:group_detail", group_id=group.id)


def idea_detail(request, group_id, idea_id):
    group = get_object_or_404(Group, id=group_id)
    idea = get_object_or_404(Idea, id=idea_id, group=group)

    context = {
        "group": group,
        "idea": idea,
    }
    return render(request, "group/group_idea_detail.html", context)


def idea_download(request, group_id, idea_id):
    group = get_object_or_404(Group, id=group_id)
    idea = get_object_or_404(Idea, id=idea_id, group=group)

    file_path = idea.file.path

    fs = FileSystemStorage(file_path)
    content_type, _ = mimetypes.guess_type(file_path)

    response = FileResponse(fs.open(file_path, "rb"),
                            content_type=f"{content_type}")
    response[
        "Content-Disposition"] = f'attachment; filename="{file_path.split("/")[-1]}"'
    return response


def vote_create(request, group_id):
    group = Group.objects.get(pk=group_id)
    user = request.user

    try:
        user_state, created = MemberState.objects.get_or_create(user=user,
                                                                group=group)

        if request.method == "POST":
            form = VoteForm(request.POST, group_id=group.id)
            if form.is_valid():
                vote = form.save(commit=False)
                vote.user = user
                vote.group = group

                idea_vote1_id = (form.cleaned_data["idea_vote1"].id
                                 if form.cleaned_data["idea_vote1"] else None)
                idea_vote2_id = (form.cleaned_data["idea_vote2"].id
                                 if form.cleaned_data["idea_vote2"] else None)
                idea_vote3_id = (form.cleaned_data["idea_vote3"].id
                                 if form.cleaned_data["idea_vote3"] else None)

                idea_vote1 = Idea.objects.get(id=idea_vote1_id)
                idea_vote2 = Idea.objects.get(id=idea_vote2_id)
                idea_vote3 = Idea.objects.get(id=idea_vote3_id)

                idea_vote1.votes += 1
                idea_vote2.votes += 1
                idea_vote3.votes += 1

                idea_vote1.save()
                idea_vote2.save()
                idea_vote3.save()

                user_state.idea_vote1 = idea_vote1
                user_state.idea_vote2 = idea_vote2
                user_state.idea_vote3 = idea_vote3
                user_state.save()

                vote.save()
                messages.success(request, "투표가 성공적으로 저장되었습니다.")
                return redirect("group:group_detail", group_id=group_id)
        else:
            messages.error(request, "중복 선택은 불가능합니다.")
            form = VoteForm(group_id=group_id)

    except MemberState.DoesNotExist:
        messages.error(request, "MemberState가 존재하지 않습니다.")
        return redirect("group_detail", group_id=group_id)

    voted_ideas = [
        user_state.idea_vote1, user_state.idea_vote2, user_state.idea_vote3
    ]
    ideas_for_voting = (Idea.objects.filter(group=group).exclude(
        author=user).exclude(
            id__in=[idea.id for idea in voted_ideas if idea is not None]))

    return render(
        request,
        "group/group_vote_create.html",
        {
            "group": group,
            "ideas_for_voting": ideas_for_voting,
            "form": form
        },
    )


def result(request, group_id):  # 최종 결과 페이지
    group = Group.objects.get(id=group_id)
    idea_list = Idea.objects.filter(
        group=group).order_by("-score")[:group.team_number]
    members = MemberState.objects.filter(group=group)

    ctx = {"idea_list": idea_list, "members": members, "group": group}

    return render(request, "group/result.html", context=ctx)


def member_preresult(request, group_id):
    group = Group.objects.get(id=group_id)
    idea_list = Idea.objects.filter(
        group=group).order_by("-score")[:group.team_number]
    user_state = MemberState.objects.filter(user=request.user,
                                            group=group).first()
    ideas_votes = {}
    if user_state:
        ideas_votes["idea_vote1_id"] = (user_state.idea_vote1.id
                                        if user_state.idea_vote1 else None)
        ideas_votes["idea_vote2_id"] = (user_state.idea_vote2.id
                                        if user_state.idea_vote2 else None)
        ideas_votes["idea_vote3_id"] = (user_state.idea_vote3.id
                                        if user_state.idea_vote3 else None)
    ctx = {
        "group": group,
        "idea_list": idea_list,
        "ideas_votes": ideas_votes,
    }

    return render(request, "preresult/preresult_member.html", ctx)


@login_required
def vote_modify(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    user = request.user

    vote, _ = Vote.objects.get_or_create(user=user, group=group)
    own_ideas = Idea.objects.filter(group=group, author=user)
    ideas_for_voting = Idea.objects.filter(group=group).exclude(author=user)

    if request.method == "POST":
        form = VoteForm(request.POST, instance=vote, group_id=group.id)
        if form.is_valid():
            vote_instance = form.save(commit=False)

            user_state = MemberState.objects.get(user=user, group=group)
            user_state.idea_vote1 = vote_instance.idea_vote1
            user_state.idea_vote2 = vote_instance.idea_vote2
            user_state.idea_vote3 = vote_instance.idea_vote3
            user_state.save()

            messages.success(request, "투표가 수정되었습니다.")
            return redirect("group:group_detail", group_id=group.id)

    else:
        form = VoteForm(instance=vote, group_id=group.id)

    return render(
        request,
        "group/group_vote_modify.html",
        {
            "form": form,
            "group": group,
            "vote": vote,
            "ideas_for_voting": ideas_for_voting,
        },
    )

# 팀빌딩 메인함수
def team_building(request, group_id):
    idea_pk_list, member_pk_list = get_pk_list(group_id)
    
    while len(member_pk_list) > 0:
        for idx in range(5):
            if len(member_pk_list) == 0:
                break
            print(idx)
            project_fitness, member_pk_list = team_scoring(idea_pk_list, member_pk_list)
            member_pk_list = check_fitness(idea_pk_list, member_pk_list, project_fitness)
        if len(member_pk_list) == 0:
            break
        idea_pk_list, _ = get_pk_list(group_id)
    
    return redirect('/')

# 팀빌딩 헬퍼 함수
# 그룹의 아이디어와 멤버 pk를 리스트에 넣어서 저장 후 리턴
def get_pk_list(group_id):
    group = Group.objects.get(id=group_id)
    idea_list = Idea.objects.filter(
        group=group).order_by("-score")[:5]
    members = MemberState.objects.filter(
        group=group)
    
    idea_pk_list = []
    member_pk_list = []
    
    for member in members:
        member_pk_list.append(member.id)
    
    for idea in idea_list:
        idea_pk_list.append(idea.id)

    return idea_pk_list, member_pk_list

# 팀빌딩 헬퍼 함수
# 팀 적합도 점수 생성
def team_scoring(idea_list, members):
    project_average_ability = []  # 나중에 "project_pick"을 만들 때 필요함. 사이클 한번당 수정이 필요함.
    members_ability = (
        []
    )  # 후에 project_average_ability와 meshigrid하여 서로 뺄 거임. 사이클 한번당 수정이 필요함.

    # member_ability 리스트에 그룹 내 모든 멤버의 실력을 저장하는 코드.
    members_ability = calculate_members_ability(members) 

    # 각 아이디어 별로 평균 실력을 리스트로 저장하는 코드.
    project_average_ability = calculate_project_average_ability(idea_list)

    members_ability, project_average_ability = np.meshgrid(
        members_ability,
        project_average_ability)  # 위의 두 리스트를 2차원 배열로 만들어 빼줄거임.

    project_pick = calculate_project_pick(members, idea_list)

    project_fitness = np.transpose(
        abs(members_ability - project_average_ability) + project_pick)

    return project_fitness, members

# 팀빌딩 헬퍼 함수
# 각 팀원의 능력치 계산
def calculate_members_ability(members):
    members_ability = []

    for member_pk in members:
        target_member_state = MemberState.objects.get(id=member_pk)
        members_ability.append(target_member_state.group_ability)
    return members_ability

# 팀빌딩 헬퍼 함수
# 각 아이디어에 할당된 멤버들의 평균 능력치를 계산함.
def calculate_project_average_ability(idea_list):
    project_average_ability = []

    for idea_pk in idea_list:
        target_idea = Idea.objects.get(id=idea_pk)
        leader = MemberState.objects.get(user=target_idea.author)
        followers = MemberState.objects.filter(user__in=target_idea.member.all())
        score = 0

        for follower in followers:
            score += follower.group_ability

        score += leader.group_ability
        score = score / (len(followers) + 1)

        project_average_ability.append(score)

    project_average_ability.sort()
    return project_average_ability

# 팀빌딩 헬퍼 함수
# 각 프로젝트 별, 팀원 별 지망을 점수화
def calculate_project_pick(members, idea_list):
    project_pick = np.zeros(
        (len(idea_list), len(members)))  # 각 인원 별로 지망도를 2차원 배열로 만들거임.

    for member_idx, member_pk in enumerate(members):
        for project_idx, project_pk in enumerate(idea_list):
            member = MemberState.objects.get(id=member_pk)
            project = Idea.objects.get(id=project_pk)

            if project == member.idea_vote1:
                project_pick[project_idx][member_idx] = 4

            elif project == member.idea_vote2:
                project_pick[project_idx][member_idx] = 3

            elif project == member.idea_vote3:
                project_pick[project_idx][member_idx] = 2

            else:
                project_pick[project_idx][member_idx] = 1

    return project_pick

# 팀빌딩 헬퍼 함수
# 팀 적합도에 따라 각 팀별로 한 명의 팀원 배치
def check_fitness(idea_list, members, project_fitness):
    # 각열에서 가장 큰숫자의 인덱스 찾기
    argmax_columns = np.argmax(project_fitness, axis=0).astype(int)
    selected_column = int(
        np.argmin(
            project_fitness[argmax_columns.astype(int),
                            range(project_fitness.shape[1])]).astype(int))
    selected_row = int(argmax_columns[selected_column])
    print(project_fitness)
    print(selected_column)
    print(selected_row)

    # arrary_update
    project_fitness = np.delete(project_fitness, selected_row, axis=0)
    project_fitness = np.delete(project_fitness, selected_column, axis=1)
    print(project_fitness)

    # 해당 그룹에 member 추가
    target_idea = Idea.objects.get(id=idea_list[selected_column])
    target_member_state = MemberState.objects.get(id=members[selected_row])
    target_idea.member.add(target_member_state.user)
    target_member_state.my_team_idea = target_idea
    print(target_idea)
    print(target_member_state)

    print(members)
    print(idea_list)
    # 추가한 member와 idea 삭제
    members.pop(selected_row)
    idea_list.pop(selected_column)
    print(members)
    print(idea_list)

    return members
