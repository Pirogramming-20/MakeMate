from django.shortcuts import render, redirect
from .forms import GroupBaseForm, GroupDetailForm

def group_base_info(request):
    if request.method == 'POST':
        form = GroupBaseForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('group:detail_set')
    else:
        form = GroupBaseForm()
        ctx = {'form': form}
        return render(request, 'setting/setting_basic.html', context=ctx)
    
def group_detail_info(request):
    if request.method == 'POST':
        form = GroupDetailForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('group:date_set')
    else:
        form = GroupDetailForm()
        ctx = {'form': form}
        return render(request, 'setting/setting_detail.html', context=ctx)
    
def group_date(request):
    return render(request, 'setting/setting_date.html')