import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.urls import reverse
from apps.common.models import User
from apps.group.models import Group, MemberState, AdminState, Idea
from apps.group.views import State, redirect_by_auth
from apps.groupSetting.forms import NonAdminInfoForm
from datetime import datetime

# Create your views here.
@login_required(login_url="common:login")
def admin_page(request, group_id):
    group_instance = get_object_or_404(Group, id=group_id)
    now = datetime.now()
    # 운영진 인원
    admin_states_users = list(group_people(group_instance, "admin"))
    # 멤버 인원
    raw_member_states_users = list(group_people(group_instance, "member"))
    # 겹치는 인원뺴주기
    admin_set = set(admin_states_users)
    member_set = set(raw_member_states_users)
    member_states_users = list(member_set - admin_set)

    state = redirect_by_auth(request.user, group_id)

    if state == State.ADMIN:
        ctx = {
            "group_instance": group_instance,
            "admin_states_users": admin_states_users,
            "member_states_users": member_states_users,
            "now": now,
        }
        return render(request, "admin/group_admin.html", ctx)
    elif state == State.WITH_HISTORY:
        redirect_url = reverse("group:group_detail", kwargs={"group_id": group_id})
        return redirect(redirect_url)
    else:
        return redirect('/')
    
# 운영진&비운영진 멤버 리스트뽑는 함수
def group_people(group_instance, state):
    if state == "admin":
        users_ids = group_instance.admin_states.values_list("user", flat=True)
    elif state == "member":
        users_ids = group_instance.member_states.values_list("user", flat=True)

    users = User.objects.filter(id__in=users_ids)
    return users

@login_required(login_url="common:login")
def group_user_delete(request, group_id, user_id):
    if request.method == "POST":
        if AdminState.objects.filter(user__id=user_id,
                                     group__id=group_id).exists():
            admin_user_state = get_object_or_404(AdminState,
                                                 user__id=user_id,
                                                 group__id=group_id)
            admin_user_state.delete()
            if MemberState.objects.filter(user__id=user_id,
                                          group__id=group_id).exists():
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
    return redirect("group_admin:admin_page", group_id=group_id)


# patch말고 일단 POST
@login_required(login_url="common:login")
def group_user_update(request, group_id, user_id):
    group = get_object_or_404(Group, id=group_id)
    if request.method == "GET":
        user = User.objects.get(id=user_id)
        user_state = MemberState.objects.get(user=user, group=group)
        form = NonAdminInfoForm(instance=user_state)
        idea = Idea.objects.filter(group=group, author=user)
        ctx = {
            "form": form,
            "group": group,
            "user_state": user_state,
            "user": user,
            "idea": idea,
        }
        
        return render(request, "admin/group_admin_modify.html", ctx)
    elif request.method == "POST":
        user_state = MemberState.objects.get(user_id=user_id, group=group)
        form = NonAdminInfoForm(request.POST, instance=user_state)
        if form.is_valid():
            form.save()
        return redirect("group_admin:admin_page", group_id=group_id)


##Admin state 추가
@csrf_exempt
@login_required(login_url="common:login")
def admin_add(request, group_id):
    user_data = json.loads(request.body)
    user = User.objects.get(id=user_data["user_id"])
    group = Group.objects.get(id=user_data["group_id"])
    # Admin_state생성
    new_admin = AdminState.objects.create(user=user, group=group)
    return JsonResponse({"group_id": group_id})


##Admin state제거
@csrf_exempt
@login_required(login_url="common:login")
def admin_delete(request, group_id):
    user_data = json.loads(request.body)
    user = User.objects.get(id=user_data["user_id"])
    group = Group.objects.get(id=user_data["group_id"])
    # Admin_state 삭제
    bye_admin = get_object_or_404(AdminState, user=user, group=group)
    bye_admin.delete()
    return JsonResponse({"message": "AdminState deleted successfully"})

def admin_idea_delete(request, group_id, user_id):
    group = get_object_or_404(Group, pk=group_id)
    author = get_object_or_404(User, pk=user_id)
    idea = Idea.objects.filter(group=group, author=author)

    if request.method == "POST":
        idea.delete()
    
    return redirect("group_admin:user_update", group_id=group_id, user_id=user_id)