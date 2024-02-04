
document.addEventListener('DOMContentLoaded', ()=> {
  const members = document.querySelectorAll('.secondary_badge');

  members.forEach((badge)=> {
    badge.addEventListener('click', ()=> {
      const userId = badge.dataset.userId;
      const jsonData = { user_id: userId, group_id: group_instance.id };

      axios.post(`/group/${group_instance.id}/admin/admin_add`, jsonData)
        .then(()=> {
          badge.classList.remove('secondary_badge');
          badge.classList.add('primary_badge');
          badge.innerText = '운영진'; 
        })
    });
  });
});

  const admins= document.querySelectorAll('.primary_badge');

  admins.forEach((badge)=>{
    badge.addEventListener('click',()=>{
      const userId =badge.dataset.userId
      const jsonData={user_id:userId,group_id:group_instance.id};

      axios.post(`/group/${group_instance.id}/admin/admin_delete`,jsonData)
        .then(()=>{
          badge.classList.remove('primary_badge');
          badge.classList.add('secondary_badge');
          badge.innerText='비운영진';
        });
    });
  });



