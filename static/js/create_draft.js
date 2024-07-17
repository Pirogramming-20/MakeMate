//groupId 정의 부분
// const currentUrl=window.location.href;
// const parts = currentUrl.split('/idea/');
// const groupId = parts.length > 1 ? parts[1].split('/')[0] : null;
// console.log(groupId)

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

// 240737 연우: 만약 group을 여러개를 들어갔다면?
const saveDraft = async () => {
    const titleInput = document.getElementById("id_title").value;
    const introInput = document.getElementById("id_intro").value;
    const contentInput = document.getElementById("id_content").value;

    const csrf_token = getCookie('csrftoken');
    const url = `/idea/draft/`;

    console.log("title: " + titleInput);
    console.log("intro: " + introInput);
    console.log("content: " + contentInput);

    const res= await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrf_token,
        },
        body: new URLSearchParams({
            'draft_title': titleInput,
            'draft_intro': introInput,
            'draft_content': contentInput
        }),
    });
    console.log(res)
    console.log(res.status)
    
    // 디버깅용
    if (res.status === "fail") {
        console.log("자동 저장에 실패했습니다.")
    }
}

// 해당 페이지를 벗어나면 임시 저장
window.addEventListener('beforeunload', saveDraft);