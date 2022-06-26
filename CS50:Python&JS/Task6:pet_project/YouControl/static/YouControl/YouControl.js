document.addEventListener('DOMContentLoaded', function() {
    // Use buttons to toggle between views

    check_post_form = document.querySelector('#new-post-form')
    if (check_post_form) {
        check_post_form.addEventListener('submit', create_post);
    }

    document.querySelectorAll('.edit-btn').forEach(item => {
        item.onclick = function() {
            edit_post(this.dataset.post);
        }
    });

    document.querySelectorAll('.delete-btn').forEach(item => {
        item.onclick = function() {
            delete_post(this.dataset.post);
        }
    });

    subscribe_btn = document.querySelector('#subscribe')

    if (subscribe_btn) {
        subscribe_btn.onclick = function() {

            btn_state = subscribe_btn.className.includes("up")
            profile_id = this.dataset.user

            subscribe(profile_id, btn_state)
            update_subscribes(profile_id, btn_state)
        }
    }
});

function create_post() {

    const post_name = document.querySelector('#post-name').value;
    const description = document.querySelector('#description').value;
    const tin = document.querySelector('#tin').value;
    const sert_num = document.querySelector('#sert_num').value;

    if (post_name && description && tin && sert_num) {

        let csrftoken = getCookie('csrftoken');

        fetch('/posts', {
            headers: {'X-CSRFToken': csrftoken},
            method: 'POST',
            body: JSON.stringify({
                post_name: post_name,
                description: description,
                tin: tin,
                sert_num: sert_num
            })
        })

    } else {
        alert("Error! Company info forms can't be empty")
    }
}

function edit_post(post_id) {

    let csrftoken = getCookie('csrftoken');

    post = document.querySelector(`#post-${post_id}`)


    edit_page_btn = document.querySelector(`#edit-page-${post_id}`)
    edit_page_btn.style.display = 'none';

    post_name = document.querySelector(`#name-${post_id}`).firstElementChild
    description = document.querySelector(`#description-${post_id}`).firstElementChild
    tin = document.querySelector(`#tin-${post_id}`).lastElementChild
    sert_num = document.querySelector(`#sert_num-${post_id}`).lastElementChild
    sert_status = document.querySelector(`#sert_status-${post_id}`).lastElementChild

    post.innerHTML = create_edit_post_form(post_id, post_name.innerHTML, description.innerHTML, tin.innerHTML, sert_num.innerHTML, sert_status.innerHTML)

    name_field = document.querySelector(`#post-name-${post_id}`)
    name_field.focus()
    name_field.selectionStart = name_field.value.length

    description_field = document.querySelector(`#post-description-${post_id}`)
    tin_field = document.querySelector(`#post-tin-${post_id}`)
    sert_num_field = document.querySelector(`#post-sert_num-${post_id}`)
    sert_status_field = document.querySelector(`#post-sert_status-${post_id}`)

    save_btn = document.querySelector(`#save-post-${post_id}`)
    save_btn.addEventListener('click', () => {
        if (name_field.value) {
            fetch(`/posts/${post_id}`, {
                headers: {'X-CSRFToken': csrftoken},
                method: 'PUT',
                body: JSON.stringify({
                    post_name: name_field.value,
                    description: description_field.value,
                    tin: tin_field.value,
                    sert_num: sert_num_field.value,
                    sert_status: sert_status_field.value,
                })
            })
            post_name.innerHTML = name_field.value
            description.innerHTML = description_field.value
            tin.innerHTML = tin_field.value
            sert_num.innerHTML = sert_num_field.value
            sert_status.innerHTML = sert_status_field.value
        }
        else {
            alert("Error! Post content can't be empty")
        }
        edit_page_btn.style.display = 'block';
    })

    cancel_btn = document.querySelector(`#cancel-edit-${post_id}`)
    cancel_btn.addEventListener('click', () => {

        fetch(`/posts/${post_id}`)
            .then(response => response.json())
            .then(result => {
                post_name.innerHTML = `${result.post_name}`,
                description.innerHTML = `${result.description}`,
                tin.innerHTML = `${result.tin}`,
                sert_num.innerHTML = `${result.sert_num}`,
                sert_status.innerHTML = `${result.sert_status}`
            });
        edit_page_btn.style.display = 'block';
    })
}

function create_edit_post_form(post_id, post_name, description, tin, sert_num, sert_status) {

    const edit_form = document.createElement('form');
    edit_form.id = `edit-form-${post_id}`;
    edit_form.innerHTML = `<input class="form-control" id="post-name-${post_id}" value="${post_name}">
        <input class="form-control" id="post-description-${post_id}" value="${description}">
        <input class="form-control" id="post-tin-${post_id}" value="${tin}">
        <input class="form-control" id="post-sert_num-${post_id}" value="${sert_num}">
        <input class="form-control" id="post-sert_status-${post_id}" value="${sert_status}">
        <input type="submit" class="btn btn-primary" id="save-post-${post_id}" value="Save"/>
        <button class="btn btn-primary" id="cancel-edit-${post_id}">Cancel</button>`;

    return edit_form.innerHTML
}

function subscribe(profile_id, state) {

    let csrftoken = getCookie('csrftoken');

    fetch(`/follows/${profile_id}`, {
        headers: {'X-CSRFToken': csrftoken},
        method: 'PUT',
        body: JSON.stringify({
            following: profile_id
        })
    })
}

function update_subscribes(profile_id, btn_state) {

    subscribe_btn = document.querySelector('#subscribe')
    followers = document.querySelector('#followers').innerHTML

    if (btn_state) {
        subscribe_btn.className = "btn down"
        subscribe_btn.firstElementChild.innerHTML = "<strong>Unsubscribe</strong>"
        subscribe_btn.blur()
        followers++;
    }
    else {
        subscribe_btn.className = "btn up"
        subscribe_btn.firstElementChild.innerHTML = "<strong>Subscribe</strong>"
        subscribe_btn.blur()
        followers--;
    }

    document.querySelector('#followers').innerHTML = followers;

}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
