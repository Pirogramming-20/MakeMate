from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Group, MemberState, AdminState, Idea 
from .forms import GroupPasswordForm, NonAdminInfoForm, GroupBaseForm, GroupDetailForm, GroupDateForm, IdeaForm, VoteForm
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

group_title = None
group_team_number = None
group_password = None
group_type = None
group_ability_description1 = None
group_ability_description2 = None
group_ability_description3 = None
group_ability_description4 = None
group_ability_description5 = None
group_choice = None
group_tech_stack = None
group_end_date = None

# Create your views here.
@login_required(login_url='common:login')
def check_nonadmin(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    state = redirect_by_auth(request.user, group_id) # 권한에 따른 리다이렉트
    wrong_flag = False # 비밀번호가 틀리면 화면에 에러 렌더링

    if state == 0: # 이전 인증 내역이 있을 경우
        return redirect(f'/group/{group_id}/') 
    
    elif state == 2: # 운영진인 경우
        return redirect(f'/group/{group_id}/admin/')
    
    if request.method == 'POST':
        form = GroupPasswordForm(request.POST)
        if form.is_valid():
            password_form = form.save(commit=False)

            if group.password == password_form.password: # 비밀번호가 일치했을 때
                new_state = MemberState()
                new_state.group = group
                new_state.user = request.user
                new_state.save()
                return redirect(f'/group/{group_id}/non_admin_info/')
            else:
                wrong_flag = True  
    form = GroupPasswordForm()
    ctx = {
        'group': group,
        'is_wrong': wrong_flag,
        'form': form
    }
    return render(request, 'group/group_certification.html', ctx)

# Create your views here.
@login_required(login_url='common:login')
def check_admin(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    state = redirect_by_auth(request.user, group_id) # 권한에 따른 리다이렉트
    wrong_flag = False # 비밀번호가 틀리면 화면에 에러 렌더링

    if state == 0: # 참여자인 경우
        return redirect(f'/group/{group_id}/') 
    
    elif state == 1: # 이미 인증 내역이 있는 경우
        return redirect(f'/group/{group_id}/admin')
    
    if request.method == 'POST':
        form = GroupPasswordForm(request.POST)
        if form.is_valid():
            password_form = form.save(commit=False)
            if group.password == password_form.password: # 비밀번호가 일치했을 때
                new_state = MemberState()
                new_state.group = group
                new_state.user = request.user
                new_state.save()
                return redirect(f'/group/{group_id}/admin')
            else:
                wrong_flag = True  
    form = GroupPasswordForm()
    ctx = {
        'group': group,
        'is_wrong': wrong_flag,
        'form': form
    }
    return render(request, 'group/group_certification.html', ctx)

def info_nonadmin(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    state = redirect_by_auth(request.user, group_id) # 권한에 따른 리다이렉트
    user_state = MemberState.objects.filter(
        user = request.user,
        group_id = group_id
    ).first()
    
    if state == 2: # 운영진인 경우
        return redirect(f'/group/{group_id}/admin/')
    
    if request.method == 'POST':
        form = NonAdminInfoForm(request.POST, instance=user_state)
        if form.is_valid():
            form.save()
            return redirect(f'/group/{group_id}/')
    form = NonAdminInfoForm()
    ctx = {
        'group': group,
        'form': form
    }
    return render(request, 'group/group_member_info.html', ctx)

def redirect_by_auth(user, group_id):
    user_state = MemberState.objects.filter(
        user = user,
        group_id = group_id
    ).first()

    admin_state = AdminState.objects.filter(
        user = user,
        group_id = group_id
    ).first()

    # 운영진인 경우
    if admin_state:
        return 2
    
    # 이전에 작성한 내역이 있을 경우
    if user_state and user_state.group is not None:
        return 0
    
    # 참여자인 경우
    return 1

def group_base_info(request):
    global group_title, group_team_number, group_password, group_type
    if request.method == 'POST':
        form = GroupBaseForm(request.POST)
        if form.is_valid():
            group_title = form.cleaned_data['title']
            group_team_number = form.cleaned_data['team_number']
            group_password = form.cleaned_data['password']
            group_type = form.cleaned_data['type']
        return redirect('group:detail_set')
    else:
        form = GroupBaseForm()
        ctx = {'form': form}
        return render(request, 'setting/setting_basic.html', context=ctx)
    
def group_detail_info(request):
    global group_ability_description1, group_ability_description2, group_ability_description3
    global group_ability_description4, group_ability_description5, group_choice, group_tech_stack
    if request.method == 'POST':
        form = GroupDetailForm(request.POST)
        if form.is_valid():
            group_ability_description1 = form.cleaned_data['ability_description1']
            group_ability_description2 = form.cleaned_data['ability_description2']
            group_ability_description3 = form.cleaned_data['ability_description3']
            group_ability_description4 = form.cleaned_data['ability_description4']
            group_ability_description5 = form.cleaned_data['ability_description5']
            group_choice = form.cleaned_data['choice']
            group_tech_stack = form.cleaned_data['tech_stack']
        return redirect('group:date_set')
    else:
        form = GroupDetailForm()
        ctx = {'form': form}
        return render(request, 'setting/setting_detail.html', context=ctx)
    
def group_date(request):
    global group_title, group_end_date
    if request.method == 'POST':
        form = GroupDateForm(request.POST)
        if form.is_valid():
            group_end_date = form.cleaned_data['end_date']

            group = Group.objects.create(
                title=group_title,
                team_number=group_team_number,
                password=group_password,
                type=group_type,
                ability_description1=group_ability_description1,
                ability_description2=group_ability_description2,
                ability_description3=group_ability_description3,
                ability_description4=group_ability_description4,
                ability_description5=group_ability_description5,
                choice=group_choice,
                tech_stack=group_tech_stack,
                end_date=group_end_date
            )
        return redirect('group:group_detail', group_id=group.id)
    else:
        form = GroupDateForm()
        ctx = {'form': form}
        return render(request, 'setting/setting_date.html', context=ctx)
    
def share(request, pk):
    pass

 
def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    author_ideas = Idea.objects.filter(group=group, author=request.user)
    other_ideas = Idea.objects.filter(group=group).exclude(author=request.user)
    user_state = MemberState.objects.filter(user=request.user, group=group).first()
    
    ideas_votes = {}
    if user_state:
        ideas_votes['idea_vote1_id'] = user_state.idea_vote1.id if user_state.idea_vote1 else None
        ideas_votes['idea_vote2_id'] = user_state.idea_vote2.id if user_state.idea_vote2 else None
        ideas_votes['idea_vote3_id'] = user_state.idea_vote3.id if user_state.idea_vote3 else None

    ctx = {
        'group': group,
        'author_ideas': author_ideas,
        'other_ideas': other_ideas,
        'ideas_votes': ideas_votes,
    }
    return render(request, 'group/group_detail.html', ctx)



def idea_create(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.method == 'POST':
        form = IdeaForm(request.POST, request.FILES)
        if form.is_valid():
            idea = form.save(commit=False)
            idea.group = group
            idea.author = request.user 
            idea.save()
            return redirect('group:group_detail', group_id=group.id)
    else:
        form = IdeaForm()
    ctx = {
        'form' : form,
        'group' : group,
    }
    return render(request, 'group/group_idea_create.html', ctx)
    

def idea_modify(request, group_id, idea_id):
    group = get_object_or_404(Group, id=group_id)
    idea = get_object_or_404(Idea, id=idea_id, group=group, author=request.user)

    if request.method == 'POST':
        form = IdeaForm(request.POST, request.FILES, instance=idea)
        if form.is_valid():
            form.save()
            return redirect('group:idea_detail', group_id=group.id, idea_id=idea.id) 
    else:
        form = IdeaForm(instance=idea)

    
    ctx = {
        'form' : form,
        'group' : group,
        'idea' : idea,
        }
    return render(request, 'group/group_idea_modify.html', ctx)

def idea_delete(request, group_id, idea_id):
    group = get_object_or_404(Group, id=group_id)
    idea = get_object_or_404(Idea, id=idea_id, group=group, author=request.user)

    if request.method == 'POST' and request.POST.get('action') == 'delete':
        idea.delete()
        return redirect('group:group_detail', group_id=group.id)
    
def idea_detail(request, group_id, idea_id):
    group = get_object_or_404(Group, id=group_id)
    idea = get_object_or_404(Idea, id=idea_id, group=group)
    
    context = {
        
        'group': group,
        'idea': idea,
    }
    
    return render(request, 'group/group_idea_detail.html', context)



def vote_create(request, group_id):
    group = Group.objects.get(pk=group_id)
    user = request.user

    try:
        # MemberState를 검색하거나 생성하기
        user_state, created = MemberState.objects.get_or_create(user=user, group=group)

        if request.method == 'POST':
            form = VoteForm(request.POST)
            if form.is_valid():
                # Vote 객체 생성
                vote = form.save(commit=False)
                vote.user = user
                vote.group = group
                # 폼에서 선택한 1지망, 2지망, 3지망 아이디어의 ID를 가져옵니다.
                idea_vote1_id = form.cleaned_data['idea_vote1'].id if form.cleaned_data['idea_vote1'] else None
                idea_vote2_id = form.cleaned_data['idea_vote2'].id if form.cleaned_data['idea_vote2'] else None
                idea_vote3_id = form.cleaned_data['idea_vote3'].id if form.cleaned_data['idea_vote3'] else None

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
                messages.success(request, '투표가 성공적으로 저장되었습니다.')
                return redirect('group:group_detail', group_id=group_id)
        else:
            form = VoteForm()
    except MemberState.DoesNotExist:
        # MemberState가 없는 경우 처리
        messages.error(request, 'MemberState가 존재하지 않습니다.')
        return redirect('group_detail', group_id=group_id)            
    # GET 요청인 경우, 투표하기 폼을 렌더링합니다.
    voted_ideas = [user_state.idea_vote1, user_state.idea_vote2, user_state.idea_vote3]
    ideas_for_voting = Idea.objects.filter(group=group).exclude(id__in=[idea.id for idea in voted_ideas if idea is not None])
    
    return render(request, 'group/group_vote_create.html', {'group': group, 'ideas_for_voting': ideas_for_voting, 'form': form})
