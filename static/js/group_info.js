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
    data = new URLSearchParams(formData).toString()

    const res = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrfToken,
        },
        body: data,
    });

    const response = await res.json();
    console.log(response)
    
    if (response.state === 0) {
        document.getElementById('state_desc').innerHTML = 'STEP 1. 기본 정보 작성';
        document.getElementById('base_set_submit_btn').onclick = () => changeStage(0);
    }
    if (response.state === 1) {
        document.getElementById('state_desc').innerHTML = 'STEP 2. 상세 설정';
        document.getElementById('form_container').innerHTML = response.form_html;
        document.getElementById('base_set_submit_btn').onclick = () => changeStage(1);
    }
    if (response.state === 2) {
        document.getElementById('state_desc').innerHTML = 'STEP 3. 결과 발표 일정';
        document.getElementById('form_container').innerHTML = response.form_html;
        document.getElementById('base_set_submit_btn').onclick = () => changeStage(2);
    }
    if (response.state === 3) {
        const redirect_url = '/group/share/';
        window.location.href = redirect_url;
    }
}