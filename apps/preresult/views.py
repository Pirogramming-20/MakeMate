from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.urls import reverse
from apps.group.models import Group, MemberState, Idea
from apps.group.views import State, TeamNumber, redirect_by_auth 

# Create your views here.
@login_required(login_url="common:login")
def preresult(request, group_id):
    # 그룹에 있는 아이디어를 모두 가져오고, 이를 투표점수 순서로 정렬
    # 그리고 동점자 처리도 해야하는데 그건 추후 다같이 결정
    group = Group.objects.get(id=group_id)
    idea_list = Idea.objects.filter(
        group=group).order_by("-score")[:TeamNumber.THIRD_TEAM.value]
    members = MemberState.objects.filter(group=group)
    state = redirect_by_auth(request.user, group_id)

    current_time = timezone.now()
    if current_time >= group.end_date:
        if state == State.ADMIN:
            ctx = {"idea_list": idea_list, "members": members, "group": group}
            return render(request, "preresult/preresult_admin.html", context=ctx)
        else:
            return redirect('/')
    else:
        redirect_url = reverse("group:group_detail", kwargs={"group_id": group_id})
        return redirect(redirect_url)

@login_required(login_url="common:login")
def member_preresult(request, group_id):
    group = Group.objects.get(id=group_id)
    idea_list = Idea.objects.filter(
        group=group).order_by("-score")[:TeamNumber.THIRD_TEAM.value]
    user_state = MemberState.objects.filter(user=request.user,
                                            group=group).first()
    state = redirect_by_auth(request.user, group_id)

    current_time = timezone.now()
    if current_time >= group.end_date:
        if (state == State.WITH_HISTORY or state == State.ADMIN):
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
        else:
            return redirect('/')
    else:
        redirect_url = reverse("group:group_detail", kwargs={"group_id": group_id})
        return redirect(redirect_url)

@login_required(login_url="common:login")
def preresult_modify(request, group_id):
    group = Group.objects.get(id=group_id)
    idea_list = Idea.objects.filter(
        group=group).order_by("-score")[:TeamNumber.THIRD_TEAM.value]
    members = MemberState.objects.filter(group=group, group_ability__isnull=False)
    state = redirect_by_auth(request.user, group_id)

    current_time = timezone.now()
    if current_time >= group.end_date:
        if state == State.ADMIN:
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
                        url = reverse("preresult:preresult", args=[group.id])
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

                url = reverse("preresult:preresult", args=[group.id])
                return redirect(url)
            else:
                ctx = {
                    "members": members,
                    "idea_list": idea_list,
                    "group": group,
                }
                return render(request, "preresult/preresult_modify.html", context=ctx)
        else:
            return redirect('/')
    else:
        redirect_url = reverse("group:group_detail", kwargs={"group_id": group_id})
        return redirect(redirect_url)