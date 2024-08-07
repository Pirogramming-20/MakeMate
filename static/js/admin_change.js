const getGroupId = (currentUrl, seperate) => {
  const parts = currentUrl.split(seperate);
  const groupId = parts.length > 1 ? parts[1].split('/')[0] : null;
  return groupId
}

//groupId 정의 부분
const currentUrl = window.location.href;
const groupId = getGroupId(currentUrl, '/group_admin/');

document.addEventListener('click', (event)=> {
  const clickedBadge=event.target;
  //비운영진 뱃지일때
  if (clickedBadge.classList.contains('cta_blue_badge')){
      const userId = clickedBadge.dataset.userId;
      const jsonData = { user_id: userId, group_id: groupId  };

      axios.post(`/group_admin/${groupId}/admin_add/`, jsonData)
        .then(()=> {
          clickedBadge.classList.remove('cta_blue_badge');
          clickedBadge.classList.add('primary_badge');
          clickedBadge.innerText = '운영진'; 
        })
    //운영진 뱃지일때
  }else if (clickedBadge.classList.contains('primary_badge')){
      const userId =clickedBadge.dataset.userId
      const jsonData={user_id:userId,group_id:groupId};

      axios.post(`/group_admin/${groupId}/admin_delete/`, jsonData)
      .then(()=>{
        clickedBadge.classList.remove('primary_badge');
        clickedBadge.classList.add('cta_blue_badge');
        clickedBadge.innerText='비운영진';
    });
  };
});



