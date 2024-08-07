import mimetypes, json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from apps.group.models import Group, MemberState, Idea
from apps.idea.models import Comment
from apps.group.views import State, redirect_by_auth
from .forms import IdeaForm
from django.http import JsonResponse


# Create your views here.
@login_required(login_url="common:login")
def save_draft(request):
    if request.method == "POST":
        draft_title = request.POST.get('draft_title', '')
        draft_intro = request.POST.get('draft_intro', '')
        draft_content = request.POST.get('draft_content', '')

        # 세션에 최근 내용 저장 (업데이트)
        request.session['draft_title'] = draft_title
        request.session['draft_intro'] = draft_intro
        request.session['draft_content'] = draft_content

        ctx = {
            'status': 'success'
        }
        return JsonResponse(ctx)
    
    # POST 요청이 아닌 경우 에러 처리
    ctx = {
        'status': 'fail'
    }
    return JsonResponse(ctx)

@login_required(login_url="common:login")
def idea_create(request, group_id):
    current_time = timezone.now()
    group = get_object_or_404(Group, id=group_id)
    state = redirect_by_auth(request.user, group_id)

    if state == State.WITH_HISTORY and current_time < group.first_end_date:
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

                # 세션에 저장된 내용 삭제
                if 'draft_title' in request.session:
                    del request.session['draft_title']
                if 'draft_info' in request.session:
                    del request.session['draft_intro']
                if 'draft_content' in request.session:
                    del request.session['draft_content']
                    
                return redirect("group:group_detail", group_id=group.id)
        else:
            form = IdeaForm()

        draft_title = request.session.get('draft_title', '')
        draft_intro = request.session.get('draft_intro', '')
        draft_content = request.session.get('draft_content', '')

        request.session.save()

        ctx = {
            "form": form,
            "group": group,
            "draft_title": draft_title,
            "draft_intro": draft_intro,
            "draft_content": draft_content
        }
        return render(request, "group/group_idea_create.html", ctx)
    elif state == State.ADMIN:
        redirect_url = reverse("group:group_detail",
                               kwargs={"group_id": group_id})
        return redirect(redirect_url)
    else:
        return redirect("/")


@login_required(login_url="common:login")
def idea_modify(request, group_id, idea_id):
    group = get_object_or_404(Group, id=group_id)
    idea = get_object_or_404(Idea,
                             id=idea_id,
                             group=group,
                             author=request.user)
    state = redirect_by_auth(request.user, group_id)

    if state == State.WITH_HISTORY:
        if request.method == "POST":
            if "file-clear" in request.POST and idea.file:
                idea.file.delete()
                idea.file = None
                idea.save(update_fields=["file"])

            form = IdeaForm(request.POST, request.FILES, instance=idea)

            if form.is_valid():
                form.save()

                # 세션에 저장된 내용 삭제
                if 'draft_title' in request.session:
                    del request.session['draft_title']
                if 'draft_info' in request.session:
                    del request.session['draft_intro']
                if 'draft_content' in request.session:
                    del request.session['draft_content']

                idea = get_object_or_404(Idea,
                                         id=idea_id,
                                         group=group,
                                         author=request.user)  # 이 부분 추가
                return redirect("idea:idea_detail",
                                group_id=group.id,
                                idea_id=idea.id)

        else:
            form = IdeaForm(instance=idea)

        file_url = idea.file.url if idea.file else None

        # 페이지 렌더 시 임시저장된 내용 불러오기
        draft_title = request.session.get('draft_title', '')
        draft_intro = request.session.get('draft_intro', '')
        draft_content = request.session.get('draft_content', '')

        request.session.save()

        ctx = {
            "form": form,
            "group": group,
            "idea": idea,
            "file_url": file_url,
            "draft_title": draft_title,
            "draft_intro": draft_intro,
            "draft_content": draft_content
        }
        return render(request, "group/group_idea_modify.html", ctx)
    elif state == State.ADMIN and idea is None:
        redirect_url = reverse("group:group_detail",
                               kwargs={"group_id": group_id})
        return redirect(redirect_url)
    else:
        return redirect("/")


@login_required(login_url="common:login")
def idea_delete(request, group_id, idea_id):
    group = get_object_or_404(Group, id=group_id)
    idea = get_object_or_404(Idea,
                             id=idea_id,
                             group=group,
                             author=request.user)
    state = redirect_by_auth(request.user, group_id)

    if state == State.WITH_HISTORY:
        if request.method == "POST" and request.POST.get("action") == "delete":
            idea.delete()
            return redirect("group:group_detail", group_id=group.id)
        else:
            return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))

    elif state == State.ADMIN:
        idea.delete()
        return redirect("group:group_detail", group_id=group_id)
    return redirect("group:group_detail", group_id=group_id)


@login_required(login_url="common:login")
def idea_detail(request, group_id, idea_id):
    group = get_object_or_404(Group, id=group_id)
    idea = get_object_or_404(Idea, id=idea_id, group=group)
    comments = idea.comments.all()
    user_state = MemberState.objects.filter(user=request.user,
                                            group=group).first()

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

    has_voted = user_state and (user_state.idea_vote1 or user_state.idea_vote2
                                or user_state.idea_vote3)
    ctx = {
        "group": group,
        "idea": idea,
        "ideas_votes": ideas_votes,
        "has_voted": has_voted,
        'comments': comments
    }
    return render(request, "group/group_idea_detail.html", ctx)



@csrf_exempt
def comment(request):
    req = json.loads(request.body)
    idea_id = req['id']
    comment_content = req['comment']

    pos = Idea.objects.get(id=idea_id)
    comment = Comment.objects.create(
        idea = pos,
        author = request.user,
        content = comment_content
    )
    
    return JsonResponse({'id': comment.id, 'user': request.user.username, 'content': comment_content})
    
@csrf_exempt
def comment_delete(request):
    req = json.loads(request.body)
    comment_id = req['comment_id']

    comment = Comment.objects.get(id=comment_id)
    comment.delete()

    return JsonResponse({'id': comment_id})


@login_required(login_url="common:login")
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
