// modal content invite members
var modal_invite_member = document.getElementById("modal-invite-member");
var btn_invite_member = document.getElementById("btn-invite-member"); 
var span = document.getElementsByClassName("close")[0]; 

btn_invite_member .onclick = function() {
    modal_invite_member.style.display = "block";
}

span.onclick = function() {
    modal_invite_member.style.display = "none"; 
}

window.onclick = function(event) {
    if (event.target == modal) {
        modal_invite_member.style.display = "none";
    }
}


// copy invite url
function CopyInviteUrl() {
    // Get the text field
    var copyText = document.getElementById("invite-url-member");
  
    // Select the text field
    copyText.select(); 
    copyText.setSelectionRange(0, 99999); // For mobile devices
  
    // Copy the text inside the text field
    navigator.clipboard.writeText(copyText.value);
  
    // Alert the copied text
    alert("Посилання скопійовано: " + copyText.value);
  }