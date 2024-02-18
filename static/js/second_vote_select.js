//groupId 정의 부분
const currentUrl=window.location.href;
const parts = currentUrl.split('/preresult/');
groupId = parts.length > 1 ? parts[1].split('/')[0] : null;


document.addEventListener('click',(event)=> {
  const clickedBadge=event.target;
  //선택 되기 전 뱃지
  if (clickedBadge.classList.contains('secondary_badge')){
    const ideaId=clickedBadge.dataset.ideaId;
    const jsonData={ idea_id:ideaId,  group_id:groupId };
    axios.post(`/preresult/${groupId}/admin/vote2/preresult/select`, jsonData)
      .then(()=>{
        clickedBadge.classList.remove('secondary_badge');
        clickedBadge.classList.add('primary_badge');
      })
  }else if (clickedBadge.classList.contains('primary_badge')){
    const ideaId=clickedBadge.dataset.ideaId;
    const jsonData={idea_id:ideaId, group_id:groupId};
    axios.post(`/preresult/${groupId}/admin/vote2/preresult/unselect`,jsonData)
    .then(() => {
      clickedBadge.classList.remove('primary_badge');
      clickedBadge.classList.add('secondary_badge');
    })
  }
});
