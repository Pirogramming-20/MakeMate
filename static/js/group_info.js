let state = 0;
let prev_data = new FormData();
let prev_data_query = new URLSearchParams(prev_data).toString();

document.getElementById('base_set_submit_btn').addEventListener('click', async ()=>{
    prev_data_query = await changeStage(state, prev_data);
})

async function changeStage(local_state, prev_data) {
    const url = '/setting/base_set/';
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
        const next_stage_html = [
            `
    <p>
        <p>실력<p>
        <span class="form_highlight_content">실력은 1(낮은 실력)부터 5(높은 실력)까지 입력 가능합니다.</span>
        <span class="form_highlight_content">각 실력에 대한 설명을 작성할 수 있습니다.</span>
    </p>
    <p>
        <label for="id_ability_description1">실력1 설명</label>
        <input type="text" name="ability_description1" maxlength="100" id="id_ability_description1">
    </p>
    <p>
        <label for="id_ability_description2">실력2 설명</label>
        <input type="text" name="ability_description2" maxlength="100" id="id_ability_description2">
    </p>
    <p>
        <label for="id_ability_description3">실력3 설명</label>
        <input type="text" name="ability_description3" maxlength="100" id="id_ability_description3">
    </p>
    <p>
        <label for="id_ability_description4">실력4 설명</label>
        <input type="text" name="ability_description4" maxlength="100" id="id_ability_description4">
    </p>
    <p>
        <label for="id_ability_description5">실력5 설명:</label>
        <input type="text" name="ability_description5" maxlength="100" id="id_ability_description5">
    </p>
    `,
    `
    <p>결과 임시 발표일</p>
    <span class="form_highlight_content">운영진에게 임시 결과가 발표되는 날짜를 설정합니다. 운영진은 결과를 수정할 수 있습니다.</span>
    <span class="form_highlight_content">투표는 임시 발표일까지 운영되며, 이후에는 투표가 불가능합니다.</span>
    <p>
        <label>1차 투표 마감일 <i class="form_highlight_content">*</i></label>
        <input type="date" name="first_end_date_0" required id="id_first_end_date_0"><input type="time" name="first_end_date_1" required id="id_first_end_date_1">       
    </p>
    <p>
        <label>2차 투표 마감일 <i class="form_highlight_content">*</i></label>
        <input type="date" name="second_end_date_0" required id="id_second_end_date_0"><input type="time" name="second_end_date_1" required id="id_second_end_date_1">   
    </p>
    <p>
        <label>3차 투표 마감일 <i class="form_highlight_content">*</i></label>
        <input type="date" name="third_end_date_0" required id="id_third_end_date_0"><input type="time" name="third_end_date_1" required id="id_third_end_date_1">
    </p>
    `
        ]
        if (local_state < 2){
            document.getElementById('state_desc').innerHTML = next_state_messages[local_state];
            document.getElementById('form_container').innerHTML = next_stage_html[local_state];

            state += 1;
        }
        else {
            window.location.href = `/setting/share/${response.group_id}`;
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

        return prev_data_query
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
    const target_first_input = document.getElementById(`id_first_end_date_1`);
    const target_second_input = document.getElementById(`id_second_end_date_1`);
    const target_third_input = document.getElementById(`id_third_end_date_1`);
    
    if ('first_end_date' in response.errors) {
        const error_msg = response.errors[`first_end_date`];
        target_first_input.insertAdjacentHTML('afterend', `
            <div class='wrap_error'>
                <span>${error_msg}</span>
            </div>
        `);
    }
    if ('second_end_date' in response.errors) {
        const error_msg = response.errors[`second_end_date`];
        target_second_input.insertAdjacentHTML('afterend', `
            <div class='wrap_error'>
                <span>${error_msg}</span>
            </div>
        `);
    }
    if ('third_end_date' in response.errors) {
        const error_msg = response.errors[`third_end_date`];
        target_third_input.insertAdjacentHTML('afterend', `
            <div class='wrap_error'>
                <span>${error_msg}</span>
            </div>
        `);
    }

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