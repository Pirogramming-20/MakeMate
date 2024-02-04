import json
from urllib.parse import parse_qs
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponsePermanentRedirect
from .forms import GroupBaseForm, GroupDetailForm, GroupDateForm
from .models import Group

def group_base_info(request):
    if request.method == 'POST':
        # request를 딕셔너리 형태로 변환 및 state 확인
        request_dict = parse_qs(request.body.decode('utf-8'))
        data_query = request_dict['cur_data'][0]
        data_dict = parse_qs(data_query)
        req = {key: values[0] for key, values in data_dict.items()}
        print(req)

        # 이전 form 작성 정보가 있을 경우 prev_req로 저장
        if 'prev_data' in request_dict:
            prev_data_query = parse_qs(request.body.decode('utf-8'))['prev_data'][0]
            prev_data_dict = parse_qs(prev_data_query)
            prev_req = {key: values[0] for key, values in prev_data_dict.items()}
            print(prev_req)
        
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

                Group.objects.create(
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
                ctx = {
                    'state': 3,
                    'is_valid': True,
                    'prev_data': prev_req,
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

def group_share(request):
    return render(request, 'setting/setting_sharing.html')