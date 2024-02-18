//groupId 정의 부분
const currentUrl=window.location.href;
const parts = currentUrl.split('/preresult/');
groupId = parts.length > 1 ? parts[1].split('/')[0] : null;


document.addEventListener('click',(event)=> {
  const clickedBadge=event.target;
  //선택 되기 전 뱃지
  if (clickedBadge.classList.contains('cta_red_badge')){
    const ideaId=clickedBadge.dataset.ideaId;
    const jsonData={ idea_id:ideaId,  group_id:groupId };
    axios.post(`/preresult/${groupId}/admin/vote1/preresult/select`, jsonData)
      .then(()=>{
        clickedBadge.classList.remove('cta_red_badge');
        clickedBadge.classList.add('cta_blue_badge');
      })
  }else if (clickedBadge.classList.contains('cta_blue_badge')){
    const ideaId=clickedBadge.dataset.ideaId;
    const jsonData={idea_id:ideaId, group_id:groupId};
    axios.post(`/preresult/${groupId}/admin/vote1/preresult/unselect`,jsonData)
    .then(() => {
      clickedBadge.classList.remove('cta_blue_badge');
      clickedBadge.classList.add('cta_red_badge');
    })
  }
});
