from enum import Enum
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Group, MemberState, AdminState, Idea

# 유저 상태를 저장하는 ENUM
class State(Enum):
    NO_HISTORY = 0
    WITH_HISTORY = 1
    ADMIN = 2

class TeamNumber(Enum):
    THIRD_TEAM = 5
    SECOND_TEAM = 5
    FIRST_TEAM = 10

# Create your views here.
def redirect_by_auth(user, group_id):
    user_state = MemberState.objects.filter(user=user,
                                            group_id=group_id).first()

    admin_state = AdminState.objects.filter(user=user,
                                            group_id=group_id).first()

    if admin_state:
        return State.ADMIN
    
    if user_state:
        if user_state.group_ability is None:
            return State.NO_HISTORY
        else:
            return State.WITH_HISTORY

    return State.NO_HISTORY

@login_required(login_url="common:login")
def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    author_ideas = Idea.objects.filter(group=group, author=request.user)
    other_ideas = Idea.objects.filter(group=group).exclude(author=request.user)
    user_state = MemberState.objects.filter(user=request.user, group=group).first()
    has_voted = False
    
    ideas_votes = {}
    if user_state:
        
        ideas_votes["idea_vote1_id"] = user_state.idea_vote1_id
        ideas_votes["idea_vote2_id"] = user_state.idea_vote2_id
        ideas_votes["idea_vote3_id"] = user_state.idea_vote3_id
        ideas_votes["idea_vote4_id"] = user_state.idea_vote4_id
        ideas_votes["idea_vote5_id"] = user_state.idea_vote5_id
        ideas_votes["idea_vote6_id"] = user_state.idea_vote6_id
        ideas_votes["idea_vote7_id"] = user_state.idea_vote7_id
        ideas_votes["idea_vote8_id"] = user_state.idea_vote8_id
        ideas_votes["idea_vote9_id"] = user_state.idea_vote9_id
        ideas_votes["idea_vote10_id"] = user_state.idea_vote10_id

        if (user_state.idea_vote1 or user_state.idea_vote2 or user_state.idea_vote3 or user_state.idea_vote4 or user_state.idea_vote5 or user_state.idea_vote6 or user_state.idea_vote7 or user_state.idea_vote8 or user_state.idea_vote9 or user_state.idea_vote10):
            has_voted = True

        # idea를 지망 순서로 정렬
        def sort_by_vote_rank(idea):
            if idea.id == ideas_votes["idea_vote1_id"]:
                return 1
            elif idea.id == ideas_votes["idea_vote2_id"]:
                return 2
            elif idea.id == ideas_votes["idea_vote3_id"]:
                return 3
            elif idea.id == ideas_votes["idea_vote4_id"]:
                return 4
            elif idea.id == ideas_votes["idea_vote5_id"]:
                return 5
            elif idea.id == ideas_votes["idea_vote6_id"]:
                return 6
            elif idea.id == ideas_votes["idea_vote7_id"]:
                return 7
            elif idea.id == ideas_votes["idea_vote8_id"]:
                return 8
            elif idea.id == ideas_votes["idea_vote9_id"]:
                return 9
            elif idea.id == ideas_votes["idea_vote10_id"]:
                return 10
            else:
                return 11  # 1, 2, 3지망이 아닌 아이디어는 4순위로
            
        if has_voted:
            other_ideas = sorted(other_ideas, key=sort_by_vote_rank)

        ctx = {
            "group": group,
            "author_ideas": author_ideas,
            "other_ideas": other_ideas,
            "ideas_votes": ideas_votes,
            "has_voted": has_voted,
            "user_state": user_state
        }
        return render(request, "group/group_detail.html", ctx)
    else:
        return redirect('/')
