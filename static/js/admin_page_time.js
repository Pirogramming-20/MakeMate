import { calculateTimeDifference } from "./util";

const currentTime = new Date();

const adminPage_endTime=document.querySelector('.admin_endtime');
const adminEndTimeString=adminPage_endTime.getAttribute('data-admin-time');
const adminEndTime=new Date(adminEndTimeString);
const { days, hours, minutes } = calculateTimeDifference(adminEndTime);
if (days < 0 || hours < 0 || minutes < 0) {
} else {
  adminPage_endTime.innerHTML = `마감까지 남은 시간: ${days}일 ${hours}시간 ${minutes}분`;
}