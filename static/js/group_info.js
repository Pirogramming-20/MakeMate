function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

const changeStage = async (state) => {
    const url = '/group/base_set/';
    const formElement = document.querySelector('form');
    const formData = new FormData(formElement);
    const csrfToken = getCookie('csrftoken');

    formData.append('state', state);

    const res = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrfToken,
        },
        body: new URLSearchParams(formData).toString(),
    });

    console.log(formData)
}
