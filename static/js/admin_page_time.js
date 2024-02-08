const currentTime = new Date();

function calculateTimeDifference(endTime) {
  const timeDifference = endTime - currentTime;
  const days = Math.floor(timeDifference / (1000 * 60 * 60 * 24));
  const hours = Math.floor((timeDifference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  const minutes = Math.floor((timeDifference % (1000 * 60 * 60)) / (1000 * 60));

  return { days, hours, minutes };
}

const adminPage_endTime=document.querySelector('.admin_endtime');
const adminEndTimeString=adminPage_endTime.getAttribute('data-admin-time');
const adminEndTime=new Date(adminEndTimeString);
const { days, hours, minutes } = calculateTimeDifference(adminEndTime);
if (days < 0 || hours < 0 || minutes < 0) {
} else {
  adminPage_endTime.innerHTML = `마감까지 남은 시간: ${days}일 ${hours}시간 ${minutes}분`;
}