from django.db import models
from apps.group.models import Idea, Vote


# 현재 구현되어있는 vote_create를 기준으로 작성했습니다. 
# (무지망 투표 구현완료시 반영 예정)
def calculate_idea_scores(group_id):
    ideas = Idea.objects.filter(group_id=group_id)

    for idea in ideas:
        votes_count = Vote.objects.filter(
            group_id=group_id
        ).filter(
            models.Q(idea_vote1=idea) | 
            models.Q(idea_vote2=idea) | 
            models.Q(idea_vote3=idea)
        ).count()
        
        idea.votes = votes_count
        idea.save()

# preresult부분에서 calculate_idea_scores 함수를 호출하여 
# 특정 그룹의 모든 아이디어에 대한 점수를 계산하는 방식으로 생각했습니다.
# 아래는 예시
calculate_idea_scores(1) #group_id가 1인 그룹의 아이디어 점수를 계산하는 경우

