import { calculateTimeDifference } from "./util";

const currentTime = new Date();

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


