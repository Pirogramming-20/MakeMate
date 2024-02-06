import json
from urllib.parse import parse_qs
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from django.urls import reverse
from django.contrib import messages
from common.models import User
from .models import Group, MemberState, AdminState, Idea
from .forms import (
    GroupPasswordForm,
    NonAdminInfoForm,
    GroupBaseForm,
    GroupDetailForm,
    GroupDateForm,
    IdeaForm,
    VoteForm,
)


# Create your views here.
@login_required(login_url="common:login")
def check_nonadmin(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    state = redirect_by_auth(request.user, group_id)  # 권한에 따른 리다이렉트
    wrong_flag = False  # 비밀번호가 틀리면 화면에 에러 렌더링

    if state == 3:  # 이전 인증 내역이 있는 참여자
        return redirect(f"/group/{group_id}/")

    elif state == 2:  # 운영진인 경우
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


# Create your views here.
@login_required(login_url="common:login")
def check_admin(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    state = redirect_by_auth(request.user, group_id)  # 권한에 따른 리다이렉트
    wrong_flag = False  # 비밀번호가 틀리면 화면에 에러 렌더링

    if state == 1 or state == 3:  # 참여자인 경우
        return redirect(f"/group/{group_id}/")

    elif state == 2:  # 이미 인증 내역이 있는 운영진인 경우
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

    if state == 2:  # 운영진인 경우
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
            return 1  # 이전에 작성한 내역이 없는 참여자인 경우
        else:
            return 3  # 이전에 작성한 내역이 있는 참여자인 경우

    if admin_state:
        return 2  # 운영진인 경우

    return 0


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

        # 현재 state 정보 저장
        state = int(req["state"])

        # state 0 == 첫번째 작성 내용 저장 및 두번째 작성내용 렌더링
        if state == 0:
            form = GroupBaseForm(data=req)
            if form.is_valid():
                title = req["title"]
                team_number = int(req["team_number"])
                password = req["password"]
                type = req["type"]
                ctx = {
                    "form_html": GroupDetailForm().as_p(),
                    "is_valid": True,
                    "state": 1,
                    "prev_data": {
                        "title": title,
                        "team_number": team_number,
                        "password": password,
                        "type": type,
                    },
                }
                return JsonResponse(ctx)
            else:  # non field 또는 field 에러 전송
                ctx = {
                    "state": 0,
                    "is_valid": False,
                    "errors": form.errors,
                    "non_field_errors": form.non_field_errors(),
                }
                return JsonResponse(ctx)

        # state 1 == 두번째 작성 내용 저장 및 세번째 작성내용 렌더링
        elif state == 1:
            form = GroupDetailForm(data=req)
            if form.is_valid():
                for idx in range(1, 6):
                    prev_req[f"group_ability{idx}"] = req.get(
                        f"ability_description{idx}", "")

                prev_req["choice"] = int(req["choice"])
                prev_req["tech_stack"] = req["tech_stack"]

                ctx = {
                    "form_html": GroupDateForm().as_p(),
                    "is_valid": True,
                    "state": 2,
                    "prev_data": prev_req,
                }
                return JsonResponse(ctx)
            else:  # non field 또는 field 에러 전송
                ctx = {
                    "state": 1,
                    "is_valid": False,
                    "errors": form.errors,
                    "non_field_errors": form.non_field_errors(),
                }
                return JsonResponse(ctx)

        # state 2 == 세번째 작성 내용 저장 및 DB에 내용 저장
        elif state == 2:
            form = GroupDateForm(data=req)
            if form.is_valid():
                prev_req["end_date"] = form.cleaned_data["end_date"]

                group = Group.objects.create(
                    title=prev_req["title"],
                    team_number=prev_req["team_number"],
                    password=prev_req["password"],
                    type=prev_req["type"],
                    ability_description1=prev_req.get("group_ability1", ""),
                    ability_description2=prev_req.get("group_ability2", ""),
                    ability_description3=prev_req.get("group_ability3", ""),
                    ability_description4=prev_req.get("group_ability4", ""),
                    ability_description5=prev_req.get("group_ability5", ""),
                    choice=prev_req["choice"],
                    tech_stack=prev_req["tech_stack"],
                    end_date=prev_req["end_date"],
                )

                AdminState.objects.create(group=group, user=request.user)

                ctx = {
                    "state": 3,
                    "is_valid": True,
                    "group_id": group.id,
                }
                return JsonResponse(ctx)
            else:  # non field 또는 field 에러 전송
                ctx = {
                    "state": 2,
                    "is_valid": False,
                    "errors": form.errors,
                    "non_field_errors": form.non_field_errors(),
                }
                return JsonResponse(ctx)

    form = GroupBaseForm()
    ctx = {"form": form, "state": 0}
    return render(request, "setting/setting_basic.html", context=ctx)


def group_share(request, group_id):
    group = Group.objects.get(id=group_id)
    ctx = {"group": group}
    return render(request, "setting/setting_sharing.html", context=ctx)


def preresult(request, group_id):
    # 그룹에 있는 아이디어를 모두 가져오고, 이를 투표점수 순서로 정렬
    # 그리고 동점자 처리도 해야하는데 그건 추후 다같이 결정
    group = Group.objects.get(id=group_id)
    idea_list = Idea.objects.all().order_by("-score")[:group.team_number]
    members = MemberState.objects.filter(group=group)

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
    # 남은 시간 계산
    group_remain_time = onegroup_remain_time(group_instance)
    ctx["group_remain_time"] = group_remain_time
    return render(request, "admin/group_admin.html", ctx)


# 운영진&비운영진 멤버 리스트뽑는 함수
def group_people(group_instance, state):
    if state == "admin":
        users_ids = group_instance.admin_states.values_list("user", flat=True)
    elif state == "member":
        users_ids = group_instance.member_states.values_list("user", flat=True)

    users = User.objects.filter(id__in=users_ids)
    return users


# 시간 계산 함수... 반복객체가 아니어서..
def onegroup_remain_time(group):
    current_datetime = timezone.now()
    remaining_time = []
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


def group_user_delete(request, group_id, user_id):
    if request.method == "POST":
        if AdminState.objects.filter(user__id=user_id).exists():
            admin_user_state = get_object_or_404(AdminState, user__id=user_id)
            admin_user_state.delete()
        elif MemberState.objects.filter(user__id=user_id).exists():
            member_user_state = get_object_or_404(MemberState,
                                                  user__id=user_id)
            member_idea = Idea.objects.filter(author__id=user_id)
            member_idea.delete()
            member_user_state.delete()
        return redirect("group:admin_page", group_id=group_id)


# patch말고 일단 POST
def group_user_update(request, group_id, user_id):
    group = get_object_or_404(Group, id=group_id)
    print(group)
    print(user_id)
    if request.method == "GET":
        user = User.objects.get(id=user_id)
        print(user)
        user_state = MemberState.objects.get(user=user, group=group)
        print(user_state)
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
    idea_list = Idea.objects.all().order_by("-score")[:group.team_number]
    members = MemberState.objects.filter(group=group)

    if request.method == "POST":
        selected_values = request.POST.get("team_modify").split(",")
        member_id = int(selected_values[0])
        idea_id = int(selected_values[1])
        mod_mem = MemberState.objects.get(id=member_id)
        mod_idea = Idea.objects.get(id=idea_id)

        mod_mem.my_team_idea = mod_idea
        mod_mem.save()

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
        ideas_votes["idea_vote1_id"] = (user_state.idea_vote1.id
                                        if user_state.idea_vote1 else None)
        ideas_votes["idea_vote2_id"] = (user_state.idea_vote2.id
                                        if user_state.idea_vote2 else None)
        ideas_votes["idea_vote3_id"] = (user_state.idea_vote3.id
                                        if user_state.idea_vote3 else None)

    ctx = {
        "group": group,
        "author_ideas": author_ideas,
        "other_ideas": other_ideas,
        "ideas_votes": ideas_votes,
    }
    return render(request, "group/group_detail.html", ctx)


def idea_create(request, group_id):
    group = get_object_or_404(Group, id=group_id)
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


def vote_create(request, group_id):
    group = Group.objects.get(pk=group_id)
    user = request.user

    try:
        # MemberState를 검색하거나 생성하기
        user_state, created = MemberState.objects.get_or_create(user=user,
                                                                group=group)

        if request.method == "POST":
            form = VoteForm(request.POST)
            if form.is_valid():
                # Vote 객체 생성
                vote = form.save(commit=False)
                vote.user = user
                vote.group = group
                # 폼에서 선택한 1지망, 2지망, 3지망 아이디어의 ID를 가져옵니다.
                idea_vote1_id = (form.cleaned_data["idea_vote1"].id
                                 if form.cleaned_data["idea_vote1"] else None)
                idea_vote2_id = (form.cleaned_data["idea_vote2"].id
                                 if form.cleaned_data["idea_vote2"] else None)
                idea_vote3_id = (form.cleaned_data["idea_vote3"].id
                                 if form.cleaned_data["idea_vote3"] else None)

                # 각 아이디어에 투표를 추가하고, 사용자의 투표 기록을 저장합니다.
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
            form = VoteForm()
    except MemberState.DoesNotExist:
        # MemberState가 없는 경우 처리
        messages.error(request, "MemberState가 존재하지 않습니다.")
        return redirect("group_detail", group_id=group_id)
    # GET 요청인 경우, 투표하기 폼을 렌더링합니다.
    voted_ideas = [
        user_state.idea_vote1, user_state.idea_vote2, user_state.idea_vote3
    ]
    ideas_for_voting = Idea.objects.filter(group=group).exclude(
        id__in=[idea.id for idea in voted_ideas if idea is not None])

    return render(
        request,
        "group/group_vote_create.html",
        {
            "group": group,
            "ideas_for_voting": ideas_for_voting,
            "form": form
        },
    )
