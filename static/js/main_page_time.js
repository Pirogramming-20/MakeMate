const currentTime = new Date();

function calculateTimeDifference(endTime) {
  const timeDifference = endTime - currentTime;
  const days = Math.floor(timeDifference / (1000 * 60 * 60 * 24));
  const hours = Math.floor((timeDifference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  const minutes = Math.floor((timeDifference % (1000 * 60 * 60)) / (1000 * 60));

  return { days, hours, minutes };
}

const group_endTimes = document.querySelectorAll('.group_endtime');
group_endTimes.forEach(endTimeElement => {
  const groupEndTimeString = endTimeElement.getAttribute('data-group-time');
  const groupEndTime = new Date(groupEndTimeString);

  const { days, hours, minutes } = calculateTimeDifference(groupEndTime);

  if (days < 0 || hours < 0 || minutes < 0) {
  } else {
    endTimeElement.innerHTML = ` ${days}일 ${hours}시간 ${minutes}분`;
  }
});


