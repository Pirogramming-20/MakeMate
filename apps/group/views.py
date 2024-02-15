import json
import mimetypes
from enum import Enum
from urllib.parse import parse_qs
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, FileResponse
from django.utils import timezone
from django.urls import reverse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from apps.common.models import User
from .models import Group, MemberState, AdminState, Idea, Vote 

# 유저 상태를 저장하는 ENUM
class State(Enum):
    NO_HISTORY = 0
    WITH_HISTORY = 1
    ADMIN = 2

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

def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    author_ideas = Idea.objects.filter(group=group, author=request.user)
    other_ideas = Idea.objects.filter(group=group).exclude(author=request.user)
    user_state = MemberState.objects.filter(user=request.user, group=group).first()

    ideas_votes = {}
    if user_state:
        
        ideas_votes["idea_vote1_id"] = user_state.idea_vote1_id
        ideas_votes["idea_vote2_id"] = user_state.idea_vote2_id
        ideas_votes["idea_vote3_id"] = user_state.idea_vote3_id

    has_voted = user_state and (user_state.idea_vote1 or user_state.idea_vote2 or user_state.idea_vote3)

    ctx = {
        "group": group,
        "author_ideas": author_ideas,
        "other_ideas": other_ideas,
        "ideas_votes": ideas_votes,
        "has_voted": has_voted,
    }
    return render(request, "group/group_detail.html", ctx)

def result(request, group_id):
    group = Group.objects.get(id=group_id)
    idea_list = Idea.objects.all().order_by("-score")[:group.team_number]
    members = MemberState.objects.filter(group=group)

    ctx = {"idea_list": idea_list, "members": members, "group": group}

    return render(request, "group/result.html", context=ctx)
