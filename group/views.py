from django.shortcuts import render, redirect
from .forms import GroupBaseForm, GroupDetailForm, GroupDateForm
from .models import Group

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
        return redirect('/')
    else:
        form = GroupDateForm()
        ctx = {'form': form}
        return render(request, 'setting/setting_date.html', context=ctx)