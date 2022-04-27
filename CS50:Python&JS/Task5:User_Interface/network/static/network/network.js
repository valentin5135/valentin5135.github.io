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

    document.querySelectorAll('.like').forEach(item => {
        fetch(`/likes/${item.dataset.post}`)
        .then(response => response.json())
        .then(result => {

            result.forEach(like => {

                if (like.liker == item.dataset.user && like.source == item.dataset.post) {
                    item.firstElementChild.className = "fa fa-heart"
                }
                else {
                    item.firstElementChild.className = "fa fa-heart-o"
                }
            })
        })
        item.onclick = function() {
            btn_state = !item.firstElementChild.className.includes("fa-heart-o")

            like(this.dataset.post, this.dataset.user, btn_state)
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

    const content = document.querySelector('#post-content').value;

    if (content) {

        let csrftoken = getCookie('csrftoken');

        fetch('/posts', {
            headers: {'X-CSRFToken': csrftoken},
            method: 'POST',
            body: JSON.stringify({
                content: content
            })
        })

        document.querySelector('#post-content').value = ''
    } else {
        alert("Error! Post content can't be empty")
    }
}

function edit_post(post_id) {

    let csrftoken = getCookie('csrftoken');

    content = document.querySelector(`#content-${post_id}`).firstElementChild
    edit_page_btn = document.querySelector(`#edit-page-${post_id}`)
    content.innerHTML = create_edit_post_form(post_id, content.innerHTML)

    edit_page_btn.style.display = 'none';

    text_area = document.querySelector(`#post-content-${post_id}`)
    text_area.focus()
    text_area.selectionStart = text_area.value.length

    save_btn = document.querySelector(`#save-post-${post_id}`)
    save_btn.addEventListener('click', () => {
        if (text_area.value) {
            fetch(`/posts/${post_id}`, {
                headers: {'X-CSRFToken': csrftoken},
                method: 'PUT',
                body: JSON.stringify({
                    content: text_area.value
                })
            })
            content.innerHTML = text_area.value
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

                content.innerHTML = `${result.content}`;

            });
        edit_page_btn.style.display = 'block';
    })
}

function create_edit_post_form(post_id, content) {

    const edit_form = document.createElement('form');

    edit_form.id = `edit-form-${post_id}`;
    edit_form.innerHTML = `<textarea class="form-control" id="post-content-${post_id}">${content}</textarea>
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

function like(post_id, follower, btn_state) {

    let csrftoken = getCookie('csrftoken');

    fetch(`/likes/${post_id}`, {
        headers: {'X-CSRFToken': csrftoken},
        method: 'PUT',
        body: JSON.stringify({
            liker: follower
        })
    })
    .then(response => response.json())
    .then(response => {
        fetch(`/posts/${post_id}`)
        .then(response => response.json())
        .then(response => {
            document.querySelector(`#likes-${post_id}`).firstElementChild.innerHTML = response.likes;
        })
    })

    //update like button style
    like_btn = document.querySelector(`#like-btn-${post_id}`).firstElementChild

    if (btn_state) {
        like_btn.className = "fa fa-heart-o"
    }
    else {
        like_btn.className = "fa fa-heart"
    }
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
