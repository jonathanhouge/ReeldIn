async function getCSRFToken() {
    try {
        const response = await fetch("/get-csrf-token/");
        const data = await response.json();
        const csrfToken = data.csrf_token;

        return csrfToken;
    } catch (error) {
        console.error("Error fetching CSRF token:", error);
        throw error; // Rethrow the error to propagate it
    }
}
// Function to go to movie page when user clicks movie poster
function goToMoviePage(movieId) {
    window.location.href = "/movie/${movieId}";
}


// Overlay to blur background
const overlay = document.querySelector(".overlay"); 


// --- Remove friend modal elements ----
const remove_friend_modal = document.getElementById("remove_friend_modal");
const remove_friend_name = document.getElementById('remove_friend_name');
const remove_friend_button = document.getElementById('remove_confirm_button');
const remove_reject_button = document.getElementById('remove_reject_button');
const remove_friend_response = document.getElementById('remove_friend_response');

function openRemoveFriendModal(username){    // Make modal visible
    remove_friend_button.style.display = "inline-block";
    remove_reject_button.style.display =  "inline-block";
    remove_friend_name.innerHTML = "Would you like to remove " + username + " from your friends list?";
    remove_friend_modal.style.display = "block";
    overlay.classList.remove("hidden");
    remove_friend_button.onclick = function() {
        removeFriend(username);
    };
}
function closeRemoveFriendModal(){    // Make modal invisible
    overlay.classList.add("hidden");
    remove_friend_modal.style.display = "none";
}
async function removeFriend(friend_username){
    console.log("Removing friend with username: " + friend_username)
    // Make a POST request to remove friend from friends list
    const csrfToken = await getCSRFToken(); // Wait until getCSRFToken() resolves
    fetch("/accounts/remove/friend/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ username: friend_username })
    })
    .then(response => {
        if(response.status == 200){
            remove_friend_response.style.color = "green";
            remove_friend_button.style.display = "none";
            remove_reject_button.style.display = "none";
        }else{
            remove_friend_response.style.color = "red";
        }
        return response.text();
    })
    .then(data => {
        // Display response message
        remove_friend_response.innerHTML = data;
    })
    .catch(error => {
        // Display error message
        console.log("An error occured during the remove friend request: " + error);
    });
}
// --- Add friend modal elements ---
const add_friend_modal = document.getElementById("add_friend_modal");
const add_friend_response = document.getElementById("add_friend_response");
const send_friend_username = document.getElementById("send_friend_username");
function openAddFriendModal(username){    // Make modal visible
    add_friend_modal.style.display = "block";
    overlay.classList.remove("hidden");
    add_friend_response.innerHTML = "";
    send_friend_username.value = "";
}
function closeAddFriendModal(){    // Make modal invisible
    overlay.classList.add("hidden");
    add_friend_modal.style.display = "none";
}
async function sendFriendRequest(username){
    // Make a POST request to send friend request
    const csrfToken = await getCSRFToken(); // Wait until getCSRFToken() resolves\
    const name_input = send_friend_username.value;
    console.log("Sending friend request to: " + name_input)
    fetch("/accounts/send/friend/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ username: name_input })
    })
    .then(response => {
        if(response.status == 200){
            add_friend_response.style.color = "green";
        }
        else{
            add_friend_response.style.color = "red";
        }
        return response.text();
    })
    .then(data => {
        // Display response message
        add_friend_response.innerHTML = data;
    })
    .catch(error => {
        // Display error message
        console.log("An error occured during the add friend request: " + error);
    });
}


// --- Received Friend Request modal elements ---
const friend_request_modal = document.getElementById("friend_request_modal");
const friend_request_response = document.getElementById("friend_request_response");
const friend_request_text = document.getElementById("friend_request_text");
const accept_friend_button = document.getElementById("accept_friend_button");
const reject_friend_button = document.getElementById("reject_friend_button");

function openFriendRequestModal(username){
    friend_request_modal.style.display = "block";
    accept_friend_button.style.display = "inline-block";
    reject_friend_button.style.display = "inline-block";
    overlay.classList.remove("hidden");
    friend_request_response.innerHTML = "";
    friend_request_text.innerHTML = username + " has sent you a friend request! Would you like to accept?";
    accept_friend_button.onclick = function() {
        confirmFriend(username);
    };
    reject_friend_button.onclick = function() {
        rejectFriend(username);
    };
}

function closeFriendRequestModal(){
    overlay.classList.add("hidden");
    friend_request_modal.style.display = "none";
}

async function confirmFriend(friend_username){
    // Make a POST request to add friend to friends list
    const csrfToken = await getCSRFToken(); // Wait until getCSRFToken() resolves
    fetch("/accounts/accept/friend/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ username: friend_username })
    })
    .then(response => {
        if(response.status == 200){
            accept_friend_button.style.display = "none";
            reject_friend_button.style.display = "none";
            friend_request_response.style.color = "green";
        }else{
            friend_request_response.style.color = "red";
        }
        return response.text();
    })
    .then(data => {
        // Display response message
        friend_request_response.innerHTML = data;
    })
    .catch(error => {
        // Display error message
        console.log("An error occured during the accept friend request: " + error);
    });
}

async function rejectFriend(friend_username){
    // Make a POST request to reject friend request
    const csrfToken = await getCSRFToken(); // Wait until getCSRFToken() resolves

    fetch("/accounts/reject/friend/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ username: friend_username })
    })
    .then(response => {
        if(response.status == 200){
            accept_friend_button.style.display = "none";
            reject_friend_button.style.display = "none";
            friend_request_response.style.color = "green";
        }else{
            friend_request_response.style.color = "red";
        }
        return response.text();
    })
    .then(data => {
        // Display response message
        friend_request_response.innerHTML = data;
    })
    .catch(error => {
        // Display error message
        console.log("An error occured during the reject friend request: " + error);
    });
}

// --- Delete friend request modal elements ---
const delete_friend_modal = document.getElementById("delete_friend_request_modal");
const delete_friend_request_response = document.getElementById("delete_friend_request_response");
const delete_friend_request_text = document.getElementById("delete_friend_request_text");
const delete_friend_button = document.getElementById("yes_delete_friend_request_button");
const delete_reject_button = document.getElementById("no_delete_friend_request_button");

function openDeleteFriendRequestModal(username){
    delete_friend_modal.style.display = "block";
    delete_friend_request_text.innerHTML = "Would you like to delete your friend request to " + username + "?";
    overlay.classList.remove("hidden");
    delete_friend_request_response.innerHTML = "";
    delete_friend_button.style.display = "inline-block";
    delete_reject_button.style.display = "inline-block";
    delete_friend_button.onclick = function() {
        deleteFriendRequest(username);
    };
}

function closeDeleteFriendRequestModal(){
    overlay.classList.add("hidden");
    delete_friend_modal.style.display = "none";
}

async function deleteFriendRequest(friend_username){
    // Make a POST request to delete friend request
    const csrfToken = await getCSRFToken(); // Wait until getCSRFToken() resolves
    fetch("/accounts/delete/friend_request/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ username: friend_username })
    })
    .then(response => {
        if(response.status == 200){
            delete_friend_button.style.display = "none";
            delete_reject_button.style.display = "none";
            delete_friend_request_response.style.color = "green";
        }else{
            delete_friend_request_response.style.color = "red";
        }
        return response.text();
    })
    .then(data => {
        // Display response message
        delete_friend_request_response.innerHTML = data;
    })
    .catch(error => {
        // Display error message
        console.log("An error occured during the delete friend request: " + error);
    });
}

