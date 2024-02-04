function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

let state = 0;
let prev_data;

document.getElementById('base_set_submit_btn').addEventListener('click', async ()=>{
    if (state == 0){
        prev_data = await changeInitialStage(prev_data);
    }
    else if (state === 1 || state === 2) {
        prev_data = await changeStage(state, prev_data);
    }
})

function showErrors(response) {
    const wrap_errors = document.getElementsByClassName('wrap_error');
    const wrap_non_field_errors = document.getElementsByClassName('wrap_non_field_errors');
        
    // 기존 에러 메세지 지우기
    Array.from(wrap_errors).forEach((target_div) => {
        target_div.remove();
    })

    Array.from(wrap_non_field_errors).forEach((target_div) => {
        target_div.remove();
    })

    // 필드 에러 메세지 띄우기
    Object.keys(response.errors).forEach((key) => {
        const target_input = document.getElementById(`id_${key}`);
        
        target_input.insertAdjacentHTML('afterend', `
            <div class='wrap_error'>
                <span>${response.errors[key]}</span>
            </div>
        `);
    });

    // 논필드 에러 메세지 띄우기
    Object.keys(response.non_field_errors).forEach((key) => {
        const target_input = document.querySelector(form);
        
        target_input.insertAdjacentHTML('afterend', `
            <div class='wrap_non_field_errors'>
                <p>${response.non_field_errors[key]}</p>
            </div>
        `);
    });

}

function showDateErrors(response){
    const wrap_errors = document.getElementsByClassName('wrap_error');
    const wrap_non_field_errors = document.getElementsByClassName('wrap_non_field_errors');
        
    // 기존 에러 메세지 지우기
    Array.from(wrap_errors).forEach((target_div) => {
        target_div.remove();
    })

    Array.from(wrap_non_field_errors).forEach((target_div) => {
        target_div.remove();
    })

    // 필드 에러 메세지 띄우기
        const target_input = document.getElementById(`id_end_date_1`);
        console.log(target_input)
        console.log(response.errors)
        const error_msg = response.errors[`end_date`];
        
        target_input.insertAdjacentHTML('afterend', `
            <div class='wrap_error'>
                <span>${error_msg}</span>
            </div>
        `);

    // 논필드 에러 메세지 띄우기
    Object.keys(response.non_field_errors).forEach((key) => {
        const target_input = document.querySelector(form);
        
        target_input.insertAdjacentHTML('afterend', `
            <div class='wrap_non_field_errors'>
                <p>${response.non_field_errors[key]}</p>
            </div>
        `);
    });
}

async function changeInitialStage(prev_data) {
    const url = '/group/base_set/';
    const formElement = document.querySelector('form');
    const formData = new FormData(formElement);
    const csrfToken = getCookie('csrftoken');

    formData.set('state', state);
    formdata = new URLSearchParams(formData).toString()

    const res = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrfToken,
        },
        body: `cur_data=${encodeURIComponent(formdata)}`,
    });

    const response = await res.json();

    if (response.is_valid) {
        document.getElementById('state_desc').innerHTML = 'STEP 2. 상세 설정';
        document.getElementById('form_container').innerHTML = response.form_html;
        state += 1;
        const prevFormData = new URLSearchParams(response.prev_data).toString();

        return prevFormData
    }
    else {
        showErrors(response)
        return prev_data
    }
} 

async function changeStage(local_state, prev_data) {
    const url = '/group/base_set/';
    const formElement = document.querySelector('form');
    const formData = new FormData(formElement);
    const csrfToken = getCookie('csrftoken');
    
    formData.set('state', local_state);
    formdata = new URLSearchParams(formData).toString()

    const res = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrfToken,
        },
        body: `cur_data=${encodeURIComponent(formdata)}&prev_data=${encodeURIComponent(prev_data)}`,
    });

    const response = await res.json();

    if (response.is_valid){
        if (local_state == 1) {
            document.getElementById('state_desc').innerHTML = 'STEP 3. 결과 발표 일정';
            document.getElementById('form_container').innerHTML = response.form_html;

            state += 1;
        }
        else if (local_state == 2) {
            const redirect_url = '/group/share/';
            window.location.href = redirect_url;
        }
        const prevFormData = new URLSearchParams(response.prev_data).toString();
        return prevFormData
    }
    else {
        if (local_state == 1){
            showErrors(response)
        }
        else {
            showDateErrors(response)
        }
        return prev_data
    }
}

