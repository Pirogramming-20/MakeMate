let state = 0;
let prev_data = new FormData();
let prev_data_query = new URLSearchParams(prev_data).toString();

document.getElementById('base_set_submit_btn').addEventListener('click', async ()=>{
    prev_data_query = await changeInitialStage(state, prev_data);
})

async function changeInitialStage(local_state, prev_data) {
    const url = '/group/base_set/';
    const form_element = document.querySelector('form');
    const form_data = new FormData(form_element);
    const csrf_token = getCookie('csrftoken');

    form_data.set('state', state);
    const form_data_query = new URLSearchParams(form_data).toString();

    const response_promise = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrf_token,
        },
        body: `cur_data=${encodeURIComponent(form_data_query)}&prev_data=${encodeURIComponent(prev_data_query)}`,
    });

    const response = await response_promise.json();

    if (response.is_valid) {
        const next_state_messages = ['STEP 2. 상세 설정', 'STEP 3. 결과 발표 일정'];
        if (local_state < 2){
            document.getElementById('state_desc').innerHTML = next_state_messages[local_state];
            document.getElementById('form_container').innerHTML = response.form_html;

            state += 1;
        }
        else {
            window.location.href = `/group/share/${response.group_id}`;
        }
        
        return new URLSearchParams(response.prev_data).toString();
    }
    else {
        if (local_state === 2){
            showDateErrors(response);
        }
        else {
            showErrors(response);
        }

        return prev_data
    }
} 

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function showErrors(response) {
    const container = document.querySelector('form');

    clearErrorMessages();

    // 필드 에러 메세지 띄우기
    Object.keys(response.errors).forEach((key) => {
        const target_input = document.getElementById(`id_${key}`);
        
        target_input.insertAdjacentHTML('afterend', `
            <div class='wrap_error'>
                <span>${response.errors[key]}</span>
            </div>
        `);
    });

    showNonFieldErrors(response.non_field_errors, container)
}

function showDateErrors(response){
    const container = document.querySelector('form');

    clearErrorMessages();

    // 필드 에러 메세지 띄우기
    const target_input = document.getElementById(`id_end_date_1`);
    const error_msg = response.errors[`end_date`];
    
    target_input.insertAdjacentHTML('afterend', `
        <div class='wrap_error'>
            <span>${error_msg}</span>
        </div>
    `);

    showNonFieldErrors(response.non_field_errors, container);
}

function clearErrorMessages() {
    const wrap_errors = document.getElementsByClassName('wrap_error');
    const wrap_non_field_errors = document.getElementsByClassName('wrap_non_field_errors');
        
    // 기존 에러 메세지 지우기
    Array.from(wrap_errors).forEach((target_div) => {
        target_div.remove();
    })

    Array.from(wrap_non_field_errors).forEach((target_div) => {
        target_div.remove();
    })
}

function showNonFieldErrors(non_field_errors, container) {
    // 논필드 에러 메세지 띄우기
    Object.keys(non_field_errors).forEach((key) => {
        container.insertAdjacentHTML('afterend', `
            <div class='wrap_non_field_errors'>
                <p>${non_field_errors[key]}</p>
            </div>
        `);
    });
}