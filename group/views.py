from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Group, MemberState, AdminState
from .forms import GroupPasswordForm, NonAdminInfoForm

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

    if state == 0: # 이전 인증 내역이 있을 경우
        return redirect(f'/group/{group_id}/') 
    
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

