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
from apps.group.views import State, redirect_by_auth
from apps.group.models import Group, MemberState, AdminState, Idea, Vote
from .forms import IdeaForm, VoteForm

# Create your views here.
# Create your views here.
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
    return render(request, "idea/group_idea_create.html", ctx)


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
            return redirect("idea:idea_detail",
                            group_id=group.id,
                            idea_id=idea.id)
    else:
        form = IdeaForm(instance=idea)

    ctx = {
        "form": form,
        "group": group,
        "idea": idea,
    }
    return render(request, "idea/group_idea_modify.html", ctx)


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
    return render(request, "idea/group_idea_detail.html", context)


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
        return redirect("group:group_detail", group_id=group_id)

    voted_ideas = [
        user_state.idea_vote1, user_state.idea_vote2, user_state.idea_vote3
    ]
    ideas_for_voting = (Idea.objects.filter(group=group).exclude(
        author=user).exclude(
            id__in=[idea.id for idea in voted_ideas if idea is not None]))

    return render(
        request,
        "idea/group_vote_create.html",
        {
            "group": group,
            "ideas_for_voting": ideas_for_voting,
            "form": form
        },
    )

@login_required
def vote_modify(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    user = request.user

    vote, _ = Vote.objects.get_or_create(user=user, group=group)
    own_ideas = Idea.objects.filter(group=group, author=user)  
    ideas_for_voting = Idea.objects.filter(group=group).exclude(author=user)  

    if request.method == 'POST':
        form = VoteForm(request.POST, instance=vote, group_id=group.id)
        if form.is_valid():
            vote_instance = form.save(commit=False)
            
            user_state = MemberState.objects.get(user=user, group=group)
            user_state.idea_vote1 = vote_instance.idea_vote1
            user_state.idea_vote2 = vote_instance.idea_vote2
            user_state.idea_vote3 = vote_instance.idea_vote3
            user_state.save()
            
            messages.success(request, '투표가 수정되었습니다.')
            return redirect('group:group_detail', group_id=group.id)

    else:
        form = VoteForm(instance=vote, group_id=group.id)

    return render(request, 'idea/group_vote_modify.html', {
        'form': form,
        'group': group,
        'vote': vote,
        'ideas_for_voting': ideas_for_voting
    })