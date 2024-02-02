from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Group, MemberState, AdminState, Idea 
from .forms import GroupPasswordForm, NonAdminInfoForm, GroupBaseForm, GroupDetailForm, GroupDateForm, IdeaForm
# from django.db.models import Value, CharField
# from django.db.models.functions import Case, When

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
    user = request.user

    user_ideas = Idea.objects.filter(group=group, user=user)
    other_ideas = Idea.objects.filter(group=group).exclude(user=user)

    user_ideas = sorted(list(user_ideas), key=lambda idea: idea.user == user, reverse=True)
    other_ideas = list(other_ideas)

    ideas = user_ideas + other_ideas

    ctx = {
        'group': group,
        'ideas': ideas,
    }
    return render(request, 'group/group_detail.html', ctx)


def idea_create(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.method == 'POST':
        form = IdeaForm(request.POST, request.FILES)
        if form.is_valid():
            idea = form.save(commit=False)
            idea.group = group
            idea.user = request.user 
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
    idea = get_object_or_404(Idea, id=idea_id, group=group, user=request.user)

    if request.method == 'POST':
        form = IdeaForm(request.POST, request.FILES, instance=idea)
        if form.is_valid():
            form.save()
            return redirect('group:group_detail', group_id=group.id) #아니면 아이디어의 상세페이지가 나은가?
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
    idea = get_object_or_404(Idea, id=idea_id, group=group, user=request.user)

    if request.method == 'POST' and request.POST.get('action') == 'delete':
        idea.delete()
        return redirect('group:group_detail', group_id=group.id)
        
