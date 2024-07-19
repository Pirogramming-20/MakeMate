const getGroupId = (currentUrl, seperate) => {
    const parts = currentUrl.split(seperate);
    groupId = parts.length > 1 ? parts[1].split('/')[0] : null;
    return groupId
}

const getCSRF = () => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; 'csrftoken'=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

const calculateTimeDifference = (endTime) => {
    const timeDifference = endTime - currentTime;
    const days = Math.floor(timeDifference / (1000 * 60 * 60 * 24));
    const hours = Math.floor((timeDifference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((timeDifference % (1000 * 60 * 60)) / (1000 * 60));
  
    return { days, hours, minutes };
  }

export { getGroupId, getCSRF, calculateTimeDifference }