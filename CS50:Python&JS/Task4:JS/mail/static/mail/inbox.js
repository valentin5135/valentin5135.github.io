document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
    document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
    document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
    document.querySelector('#compose').addEventListener('click', compose_email);

    // By default, load the inbox
    load_mailbox('inbox');
});

function compose_email() {

    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#view-email').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';

    document.querySelector('#compose-form').onsubmit = function() {
        const recipients = document.querySelector('#compose-recipients').value;
        const subject = document.querySelector('#compose-subject').value;
        const body = document.querySelector('#compose-body').value;

        fetch('/emails', {
            method: 'POST',
            body: JSON.stringify({
                recipients: recipients,
                subject: subject,
                body: body
            })
        })
        .then(response => response.json())
        .then(result => {
            // Вивести результат в консоль
            console.log(result);
            load_mailbox('sent');
        });
    };

    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';

}

function load_mailbox(mailbox) {

    // Show the mailbox and hide other views
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#view-email').style.display = 'none';
    document.querySelector('#view-email').innerHTML = '';
    document.querySelector('#compose-view').style.display = 'none';

    // Show the mailbox name
    document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

    if(mailbox === 'inbox'){
        fetch('/emails/inbox')
        .then(response => response.json())
        .then(result => {
              // Вивести результат в консоль
            console.log(result);
            result.forEach(email => {

                const sender = document.createElement('div');
                sender.className = 'sender';
                sender.innerHTML = `<strong>${email.sender}</strong>`

                const subject = document.createElement('div');
                subject.className = 'subject';
                subject.innerHTML = `${email.subject}`

                const timestamp = document.createElement('div');
                timestamp.className = 'timestamp';
                timestamp.innerHTML = `<i>${email.timestamp}</i>`

                //create button for to create
                const arch_btn = document.createElement('button');
                arch_btn.className = 'red-arch-btn';
                arch_btn.innerHTML = '<span class="bi bi-archive red-arch-btn"></span>'

                const element = document.createElement('div');
                if (email.read === false){
                    element.className = 'each-mail';
                } else {
                    element.className = 'r-each-mail';
                }

                element.append(sender);
                element.append(subject);
                element.append(timestamp);

                const block = document.createElement('div');
                block.className = 'email-block';

                block.append(element);
                block.append(arch_btn);

                element.addEventListener('click', function() {
                    load_email(email.id);
                });

                arch_btn.addEventListener('click', function() {
                    fetch(`/emails/${email.id}`, {
                        method: 'PUT',
                        body: JSON.stringify({
                            archived: true
                        })
                    })
                    .then(() => {
                        console.log(`Email with ID : ${email.id} archivated`);
                        load_mailbox('inbox');
                    })
                });
                document.querySelector('#emails-view').append(block);
            });
        });
    } else if (mailbox === 'sent') {
        fetch('/emails/sent')
        .then(response => response.json())
        .then(result => {
            // Вивести результат в консоль
            console.log(result);
            result.forEach(email => {

                const recipients = document.createElement('div');
                recipients.className = 'recipients';
                recipients.innerHTML = `<strong>${email.recipients}</strong>`

                const subject = document.createElement('div');
                subject.className = 's-subject';
                subject.innerHTML = `${email.subject}`

                const timestamp = document.createElement('div');
                timestamp.className = 's-timestamp';
                timestamp.innerHTML = `<i>${email.timestamp}</i>`

                const element = document.createElement('div');
                element.className = 'sent-mails';

                element.append(recipients);
                element.append(subject);
                element.append(timestamp);

                element.addEventListener('click', function() {
                    load_email(email.id);
                });
                document.querySelector('#emails-view').append(element);
            });
        });
    } else if (mailbox === 'archive') {
        fetch('/emails/archive')
        .then(response => response.json())
        .then(result => {
            // Вивести результат в консоль
            console.log(result);
            result.forEach(email => {
                const sender = document.createElement('div');
                sender.className = 'sender';
                sender.innerHTML = `<strong>${email.sender}</strong>`

                const subject = document.createElement('div');
                subject.className = 'subject';
                subject.innerHTML = `${email.subject}`

                const timestamp = document.createElement('div');
                timestamp.className = 'timestamp';
                timestamp.innerHTML = `<i>${email.timestamp}</i>`

                //create button for to create
                const arch_btn = document.createElement('button');
                arch_btn.className = 'green-arch-btn';
                arch_btn.innerHTML = '<span class="bi bi-archive green-arch-btn"></span>'

                const element = document.createElement('div');
                if (email.read === false){
                    element.className = 'each-mail';
                } else {
                    element.className = 'r-each-mail';
                }

                element.append(sender);
                element.append(subject);
                element.append(timestamp);

                const block = document.createElement('div');
                block.className = 'email-block';

                block.append(element);
                block.append(arch_btn);

                element.addEventListener('click', function() {
                    load_email(email.id);
                });

                arch_btn.addEventListener('click', function() {
                    fetch(`/emails/${email.id}`, {
                        method: 'PUT',
                        body: JSON.stringify({
                            archived: false
                        })
                    })
                    .then(() => {
                        console.log(`Email with ID : ${email.id} unarchivated`);
                        load_mailbox('inbox');
                    })
                });
                document.querySelector('#emails-view').append(block);
            });
        });
    }
}

function load_email(email_id) {
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#view-email').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';

    fetch(`/emails/${email_id}`)
    .then(response => response.json())
    .then(email => {
        // Вивести лист до консолі
        console.log(email);

        const sender = document.createElement('div');
        sender.className = 'sender';
        sender.innerHTML = `<strong>From: </strong>${email.sender}`

        const recipients = document.createElement('div');
        recipients.className = 'recipients';
        recipients.innerHTML = `<strong>To: </strong>${email.recipients}`

        const subject = document.createElement('div');
        subject.className = 'subject';
        subject.innerHTML = `<strong>Subject: </strong>${email.subject}`

        const timestamp = document.createElement('div');
        timestamp.className = 'timestamp';
        timestamp.innerHTML = `<strong>Timestamp: </strong><i>${email.timestamp}</i>`

        const reply_btn = document.createElement('button');
        reply_btn.className = 'btn btn-sm btn-outline-primary';
        reply_btn.id = 'reply-btn';
        reply_btn.innerHTML = 'Reply'

        reply_btn.addEventListener('click', function() {
            reply_email(email.id)
        });

        const clear = document.createElement('hr');

        const body = document.createElement('div');
        body.className = 'email-body';
        body.innerHTML = `${email.body.replace(/\n/g,'<br>')}`

        document.querySelector('#view-email').append(sender);
        document.querySelector('#view-email').append(recipients);
        document.querySelector('#view-email').append(subject);
        document.querySelector('#view-email').append(timestamp);
        document.querySelector('#view-email').append(reply_btn);
        document.querySelector('#view-email').append(clear);
        document.querySelector('#view-email').append(body);
    });

    //mark email as read
    fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            read: true
        })
    })
    .then(() => {
        console.log(`Email with ID : ${email_id} read`);
    })
}

function reply_email(email_id) {

    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#view-email').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';

    fetch(`/emails/${email_id}`)
    .then(response => response.json())
    .then(email => {
        document.querySelector('#compose-recipients').value = email.sender;
        let exist_subject = email.subject;

        if (exist_subject.indexOf('Re:') == -1){
            document.querySelector('#compose-subject').value = `Re: ${email.subject}`
        } else {
            document.querySelector('#compose-subject').value = `${email.subject}`
        }

        document.querySelector('#compose-body').value = `\n\nOn ${email.timestamp} ${email.sender} write: ${email.body}`
    });

    document.querySelector('#compose-form').onsubmit = function() {
        const recipients = document.querySelector('#compose-recipients').value;
        const subject = document.querySelector('#compose-subject').value;
        const body = document.querySelector('#compose-body').value;

        fetch('/emails', {
            method: 'POST',
            body: JSON.stringify({
                recipients: recipients,
                subject: subject,
                body: body
            })
        })
        .then(response => response.json())
        .then(result => {
          // Вивести результат в консоль
          console.log(result);
        });
        document.querySelector('#compose-view').style.display = 'none';
        load_mailbox('sent');
    };

    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';

}
