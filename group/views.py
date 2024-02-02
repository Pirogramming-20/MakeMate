import json
from urllib.parse import parse_qs
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponsePermanentRedirect
from .forms import GroupBaseForm, GroupDetailForm, GroupDateForm
from .models import Group

new_group = Group()

def group_base_info(request):
    global new_group
    if request.method == 'POST':
        # request를 딕셔너리 형태로 변환 및 state 확인
        data_dict = parse_qs(request.body.decode('utf-8'))
        for key, values in data_dict.items():
            data_dict[key] = values[0]
        req = json.loads(json.dumps(data_dict))
        state = int(req['state'])
        print(req)

        # state 0 == 첫번째 작성 내용 저장 및 두번째 작성내용 렌더링
        if state == 0:
            form = GroupBaseForm(data=req)
            if form.is_valid():
                new_group.title = req['title']
                new_group.team_number = int(req['team_number'])
                new_group.password = req['password']
                new_group.type = req['type']
                ctx = {
                    'form_html': GroupDetailForm().as_p(),
                    'state': 1,
                }
                return JsonResponse(ctx)
        
        # state 1 == 두번째 작성 내용 저장 및 세번째 작성내용 렌더링
        elif state == 1:        
            form = GroupDetailForm(data=req)
            if form.is_valid():
                if 'group_ability1' in req:
                    new_group.group_ability1 = req['group_ability1']
                if 'group_ability2' in req:
                    new_group.group_ability2 = req['group_ability2']
                if 'group_ability3' in req:
                    new_group.group_ability3 = req['group_ability3']
                if 'group_ability4' in req:
                    new_group.group_ability4 = req['group_ability4']
                if 'group_ability5' in req:
                    new_group.group_ability5 = req['group_ability5']
                new_group.choice = int(req['choice'])
                new_group.tech_stack = req['tech_stack']
                ctx = {
                    'form_html': GroupDateForm().as_p(),
                    'state': 2,
                }
                return JsonResponse(ctx)
            
        # state 2 == 세번째 작성 내용 저장 및 리디렉션
        elif state == 2:
            form = GroupDateForm(data=req)
            if form.is_valid():
                new_group.end_date = form.cleaned_data['end_date']

                new_group.save()
                ctx = {
                    'form_html': GroupDateForm().as_p(),
                    'state': 3,
                }
                return JsonResponse(ctx)

    form = GroupBaseForm()
    ctx = {'form': form, 'state': 0}
    return render(request, 'setting/setting_basic.html', context=ctx)

def group_share(request):
    return render(request, 'setting/setting_sharing.html')