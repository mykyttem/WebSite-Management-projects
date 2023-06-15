const roomName = JSON.parse(document.getElementById('room-name').textContent);

// url
const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + roomName
    + '/'
);

// send message
chatSocket.onmessage = function(e) {
    /*
    Create elements, block message
    If my message, right side, else left 
    */

    const data = JSON.parse(e.data);
    const login_user = data.login_user; 

    var col_md_3 = document.createElement('div');
    var msg = document.createElement('div');

    tagP = document.createElement('h4');

    if (login_user !== login_session) {
        col_md_3.className = 'col-md-3';
        msg.className = 'chat-bubble chat-bubble--left';
    } else {
        col_md_3.className = 'col-md-3 offset-md-9';
        msg.className = 'chat-bubble chat-bubble--right';
    }

    tagP.textContent = data.message;
    msg.appendChild(tagP);
    col_md_3.appendChild(msg);
    document.querySelector('#chat-log .row.no-gutters').appendChild(col_md_3);
};


chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;

    chatSocket.send(JSON.stringify({
        'message': message
    }));

    messageInputDom.value = '';
};


// context menu for click on msg
var modal_msg_btn = document.getElementById("modal-btn-msg");
var btnOpenModal = document.getElementById("msg_button");
var spanClose = document.getElementsByClassName("closeBtMsg")[0];


function msg_button(id) {
    modal_msg_btn.style.display = "block";

    // get id msg and send
    var post_id_msg_click = document.getElementById("id_msg_click");
    var post_id_msg_click_edit = document.getElementById("id_msg_click_edit");
    post_id_msg_click.value = id;   
    post_id_msg_click_edit.value = id;
}  

function closeModal() {
    modal_msg_btn.style.display = "none";
}

btnOpenModal.onclick = openModal;
spanClose.onclick = closeModal;
window.onclick = function(event) {
  if (event.target == modal) {  
    closeModal();
  }
};