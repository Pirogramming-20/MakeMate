from urllib.parse import parse_qs
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Group, Idea, MemberState, AdminState
from .forms import GroupPasswordForm, NonAdminInfoForm, GroupBaseForm, GroupDetailForm, GroupDateForm

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
    if request.method == 'POST':
        # request를 딕셔너리 형태로 변환 및 state 확인
        request_dict = parse_qs(request.body.decode('utf-8'))
        data_query = request_dict['cur_data'][0]
        data_dict = parse_qs(data_query)
        req = {key: values[0] for key, values in data_dict.items()}

        # 이전 form 작성 정보가 있을 경우 prev_req로 저장
        if 'prev_data' in request_dict:
            prev_data_query = parse_qs(request.body.decode('utf-8'))['prev_data'][0]
            prev_data_dict = parse_qs(prev_data_query)
            prev_req = {key: values[0] for key, values in prev_data_dict.items()}
        
        # 현재 state 정보 저장
        state = int(req['state'])      

        # state 0 == 첫번째 작성 내용 저장 및 두번째 작성내용 렌더링
        if state == 0:
            form = GroupBaseForm(data=req)
            if form.is_valid():
                title = req['title']
                team_number = int(req['team_number'])
                password = req['password']
                type = req['type']
                ctx = {
                    'form_html': GroupDetailForm().as_p(),
                    'is_valid': True,
                    'state': 1,
                    'prev_data': {'title': title,
                                  'team_number': team_number,
                                  'password': password,
                                  'type': type},
                }
                return JsonResponse(ctx)
            else: # non field 또는 field 에러 전송
                ctx = {
                    'state': 0,
                    'is_valid': False,
                    'errors': form.errors,
                    'non_field_errors': form.non_field_errors(),
                }
                return JsonResponse(ctx)                

        
        # state 1 == 두번째 작성 내용 저장 및 세번째 작성내용 렌더링
        elif state == 1:
            form = GroupDetailForm(data=req)
            if form.is_valid():
                for idx in range(1, 6):
                    prev_req[f'group_ability{idx}'] = req.get(f'ability_description{idx}', '')

                prev_req['choice'] = int(req['choice'])
                prev_req['tech_stack'] = req['tech_stack']

                ctx = {
                    'form_html': GroupDateForm().as_p(),
                    'is_valid': True,
                    'state': 2,
                    'prev_data': prev_req,
                }
                return JsonResponse(ctx)
            else: # non field 또는 field 에러 전송
                ctx = {
                    'state': 1,
                    'is_valid': False,
                    'errors': form.errors,
                    'non_field_errors': form.non_field_errors(),
                }
                return JsonResponse(ctx) 
            
        # state 2 == 세번째 작성 내용 저장 및 DB에 내용 저장
        elif state == 2:
            form = GroupDateForm(data=req)
            if form.is_valid():
                prev_req['end_date'] = form.cleaned_data['end_date']

                group = Group.objects.create(
                    title=prev_req['title'],
                    team_number=prev_req['team_number'],
                    password=prev_req['password'],
                    type=prev_req['type'],
                    ability_description1 = prev_req.get('group_ability1', ''),
                    ability_description2 = prev_req.get('group_ability2', ''),
                    ability_description3 = prev_req.get('group_ability3', ''),
                    ability_description4 = prev_req.get('group_ability4', ''),
                    ability_description5 = prev_req.get('group_ability5', ''),
                    choice=prev_req['choice'],
                    tech_stack=prev_req['tech_stack'],
                    end_date=prev_req['end_date']
                )

                AdminState.objects.create(
                    group = group,
                    user = request.user
                )
                
                ctx = {
                    'state': 3,
                    'is_valid': True,
                    'group_id': group.id,
                }
                return JsonResponse(ctx)
            else: # non field 또는 field 에러 전송
                ctx = {
                    'state': 2,
                    'is_valid': False,
                    'errors': form.errors,
                    'non_field_errors': form.non_field_errors(),
                }
                return JsonResponse(ctx) 

    form = GroupBaseForm()
    ctx = {'form': form, 'state': 0}
    return render(request, 'setting/setting_basic.html', context=ctx)
    
def group_share(request, group_id):
    group = Group.objects.get(id=group_id)
    ctx = {'group': group}
    return render(request, 'setting/setting_sharing.html', context=ctx)

def preresult(request, group_id):
    #그룹에 있는 아이디어를 모두 가져오고, 이를 투표점수 순서로 정렬
    #그리고 동점자 처리도 해야하는데 그건 추후 다같이 결정
    group = Group.objects.get(id=group_id)
    idea_list = Idea.objects.all().order_by('-score')[:group.team_number]
    members = MemberState.objects.filter(group = group)

    #임시로 manyToMany필드에 유저값을 넣어 봤어용(확인용)
    # for idea in idea_list:
    #     for member in members:
    #         idea.member.add(member)
    #         idea.save()
    
    ctx = {
        'idea_list': idea_list,
        'members': members
    }

    return render(request, 'preresult/preresult_admin.html', context=ctx)



    

