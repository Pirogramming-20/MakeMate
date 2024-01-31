from django.shortcuts import render, redirect
from .forms import GroupBaseForm

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