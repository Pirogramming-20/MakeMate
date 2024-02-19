// const vote_btn = document.getElementById("first_vote_btn");

// vote_btn.addEventListener("click", async () => {
//     const selected = 'input[type="checkbox"]:checked';
//     const picked_idea = document.querySelectorAll(selected);
//     const csrf_token = getCookie('csrftoken');

//     const picked_idea_pk = [];
//     picked_idea.forEach((idea)=>{
//         picked_idea_pk.append(int(idea));
//     })

//     const response_promise = await fetch(url, {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/x-www-form-urlencoded',
//             'X-CSRFToken': csrf_token,
//         },
//         body: ,
//     });
// })

// function getCookie(name) {
//     const value = `; ${document.cookie}`;
//     const parts = value.split(`; ${name}=`);
//     if (parts.length === 2) return parts.pop().split(';').shift();
// }