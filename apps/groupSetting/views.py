from urllib.parse import parse_qs
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from apps.group.views import State, redirect_by_auth
from apps.group.models import Group, MemberState, AdminState
from apps.result.views import start_team_building
from apps.preresult.tasks import first_scoring_auto, second_scoring_auto, team_building_auto
from apps.preresult.views import calculate_first_idea_scores, calculate_second_idea_scores
from .forms import (
    NonAdminInfoForm,
    GroupPasswordForm,
    GroupBaseForm,
    GroupDateForm,
    GroupDetailForm,
)

# Create your views here.
# 모임 개설 메인 함수
@login_required(login_url="common:login")
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
            "password": req["password"],
        }

    if state == 1:
        for idx in range(1, 6):
            prev_req[f"group_ability{idx}"] = req.get(
                f"ability_description{idx}", "")

    if state == 2:
        prev_req["first_end_date"] = form.cleaned_data["first_end_date"]
        prev_req["second_end_date"] = form.cleaned_data["second_end_date"]
        prev_req["third_end_date"] = form.cleaned_data["third_end_date"]

    return prev_req


# 모임 개설 헬퍼 함수
# 마지막 단계에 group 데이터 저장
def save_group_data(prev_req, user):
    group = Group.objects.create(
        title=prev_req["title"],
        password=prev_req["password"],
        ability_description1=prev_req.get("group_ability1", ""),
        ability_description2=prev_req.get("group_ability2", ""),
        ability_description3=prev_req.get("group_ability3", ""),
        ability_description4=prev_req.get("group_ability4", ""),
        ability_description5=prev_req.get("group_ability5", ""),
        first_end_date=prev_req["first_end_date"],
        second_end_date=prev_req["second_end_date"],
        third_end_date=prev_req["third_end_date"],
    )

    AdminState.objects.create(group=group, user=user)

    return group


@login_required(login_url="common:login")
def check_nonadmin(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    state = redirect_by_auth(request.user, group_id)  # 권한에 따른 리다이렉트
    wrong_flag = False  # 비밀번호가 틀리면 화면에 에러 렌더링

    if state == State.WITH_HISTORY:  # 이전 인증 내역이 있는 참여자
        return redirect("common:main_page")

    elif state == State.ADMIN:  # 운영진인 경우
        return redirect("group_admin:admin_page", group_id=group.id)

    if request.method == "POST":
        form = GroupPasswordForm(request.POST)
        if form.is_valid():
            password_form = form.save(commit=False)

            if group.password == password_form.password:  # 비밀번호가 일치했을 때
                new_state = MemberState()
                new_state.group = group
                new_state.user = request.user
                new_state.save()
                return redirect("group_setting:info_nonadmin",
                                group_id=group.id)
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
        return redirect("common:main_page")

    elif state == State.ADMIN:
        return redirect("group_admin:admin_page", group_id=group.id)

    if request.method == "POST":
        form = GroupPasswordForm(request.POST)
        if form.is_valid():
            password_form = form.save(commit=False)
            if group.password == password_form.password:  # 비밀번호가 일치했을 때
                new_state = AdminState()
                new_state.group = group
                new_state.user = request.user
                new_state.save()
                return redirect("group_admin:admin_page", group_id=group.id)
            else:
                wrong_flag = True

    form = GroupPasswordForm()
    ctx = {"group": group, "is_wrong": wrong_flag, "form": form}
    return render(request, "group/group_admin_certification.html", ctx)


@login_required(login_url="common:login")
def info_nonadmin(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    state = redirect_by_auth(request.user, group_id)  # 권한에 따른 리다이렉트
    user_state = MemberState.objects.filter(user=request.user,
                                            group_id=group_id).first()
    form = NonAdminInfoForm()

    if state == State.ADMIN:  # 운영진인 경우
        return redirect("group_admin:admin_page", group_id=group.id)

    if request.method == "POST":
        form = NonAdminInfoForm(request.POST, instance=user_state)
        if form.is_valid():
            form.save()
            return redirect("common:main_page")

    ctx = {"group": group, "form": form}
    return render(request, "group/group_member_info.html", ctx)


# 팀빌딩 마지막부분에 추가
@login_required(login_url="common:login")
def group_share(request, group_id):
    group = Group.objects.get(id=group_id)

    ##팀빙딩 함수 예약
    first_scoring_auto(calculate_first_idea_scores, group)
    second_scoring_auto(calculate_second_idea_scores, group)
    team_building_auto(start_team_building, group)
    ####

    ctx = {"group": group}
    return render(request, "setting/setting_sharing.html", context=ctx)
