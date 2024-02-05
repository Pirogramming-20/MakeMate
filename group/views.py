from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Group, MemberState, AdminState
from .forms import GroupPasswordForm, NonAdminInfoForm, GroupBaseForm, GroupDetailForm, GroupDateForm

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

    if state == 3: # 이전 인증 내역이 있는 참여자
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
    return render(request, 'group/group_nonadmin_certification.html', ctx)

# Create your views here.
@login_required(login_url='common:login')
def check_admin(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    state = redirect_by_auth(request.user, group_id) # 권한에 따른 리다이렉트
    wrong_flag = False # 비밀번호가 틀리면 화면에 에러 렌더링
    
    if state == 1 or state == 3: # 참여자인 경우
        return redirect(f'/group/{group_id}/')
    
    elif state == 2: # 이미 인증 내역이 있는 운영진인 경우
        return redirect(f'/group/{group_id}/admin')
    
    if request.method == 'POST':
        form = GroupPasswordForm(request.POST)
        if form.is_valid():
            password_form = form.save(commit=False)
            if group.password == password_form.password: # 비밀번호가 일치했을 때
                new_state = AdminState()
                new_state.group = group
                new_state.user = request.user
                new_state.save()
                return redirect(f'/group/{group_id}/admin/')
            else:
                wrong_flag = True  
    form = GroupPasswordForm()
    ctx = {
        'group': group,
        'is_wrong': wrong_flag,
        'form': form
    }
    return render(request, 'group/group_admin_certification.html', ctx)

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
    
    if user_state:
        if user_state.group is None:
            return 1 # 이전에 작성한 내역이 없는 참여자인 경우
        else:
            return 3 # 이전에 작성한 내역이 있는 참여자인 경우
    
    if admin_state:
        return 2 # 운영진인 경우
    
    return 0

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
            url = reverse('group:share', args=[group.id])
        return redirect(url)
    else:
        form = GroupDateForm()
        ctx = {'form': form}
        return render(request, 'setting/setting_date.html', context=ctx)
    
def share(request, group_id):
    group = Group.objects.get(id=group_id)
    ctx = {'group': group}
    return render(request, 'setting/setting_sharing.html', context=ctx)
