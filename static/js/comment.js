const ajax_comment = (id) => {
    const detail_comment = document.querySelector('.comment_input');
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/idea/comment/', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            const { id: com_id, user: com_user, content: com_content } = JSON.parse(xhr.responseText);
            create_comment(com_id, com_user, com_content);
            detail_comment.value = null;
        }
    };

    const requestBody = JSON.stringify({ id: id, comment: detail_comment.value });
    xhr.send(requestBody);
};

const create_comment = (id, user, content) => {
    const comment_ul = document.querySelector('.detail_comment_modal ul');
    let template = `
        <div class="wrap_card">
            <div class="comment_info">
                <span class="com_nick comment_nick-{{comment.id}}">***</span>
            </div>
            <li class='comment_li-${id}'>
                <span class="com_content comment_content-${id}">${content}</span>
                <i class="fa-solid fa-trash" onclick="ajax_delete(${id})"></i>
            </li>
        </div>
    `;
    comment_ul.innerHTML += template;
};

const ajax_delete = (comment_id) => {
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/comment_delete/', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            const { id: com_id } = JSON.parse(xhr.responseText);
            delete_comment(com_id);
        }
    };

    const requestBody = JSON.stringify({ comment_id: comment_id });
    xhr.send(requestBody);
};

const delete_comment = (id) => {
    const delete_comment_span = document.querySelector(`.detail_comment_modal ul .comment_nick-${id}`);
    const delete_comment_li = document.querySelector(`.detail_comment_modal ul .comment_li-${id}`);

    delete_comment_span.remove();
    delete_comment_li.remove();
};
