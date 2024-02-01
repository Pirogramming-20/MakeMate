from django.shortcuts import render, redirect, get_object_or_404 
from .models import Idea, Group
from .forms import IdeaForm


def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    #members = group.members.all()
    ctx = {
        'group' : group,
    }
    return render(request, 'group/group_detail.html', ctx)
    

def idea_create(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.method == 'POST':
        form = IdeaForm(request.POST, request.FILES)
        if form.is_valid():
            idea = form.save(commit=False)
            idea.group = group
            idea.save()
            return redirect('group_detail', group_id=group.id)
    else:
        form = IdeaForm()
    ctx = {
        'form' : form,
        'group' : group,
    }
    return render(request, 'group/idea_create.html', ctx)
    

def idea_modify(request, group_id, idea_id):
    group = get_object_or_404(Group, id=group_id)
    idea = get_object_or_404(Idea, id=idea_id, group=group)

    if request.method == 'POST':
        form = IdeaForm(request.POST, request.FILES, instance=idea)
        if form.is_valid():
            form.save()
            return redirect('group_detail', group_id=group.id) #아니면 아이디어의 상세페이지가 나은가?
    else:
        form = IdeaForm(instance=idea)

    
    ctx = {
        'form' : form,
        'group' : group,
        'idea' : idea,
        }
    return render(request, 'group/<int:group_id>/idea', ctx)
