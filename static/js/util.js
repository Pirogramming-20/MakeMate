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

export { getGroupId, getCSRF }