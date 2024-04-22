// Function taken from landing_page.js
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
// Goes to movie page when user clicks movie poster
function goToMoviePage(movieId) {
    window.location.href = "/movie/${movieId}";
}

// Overlay element for background blur
const overlay = document.querySelector(".overlay"); 


/**
 * Remove friend functionality
 */

// elements
const remove_friend_modal = document.getElementById("remove_friend_modal");
const remove_friend_name = document.getElementById('remove_friend_name');
const remove_friend_button = document.getElementById('remove_confirm_button');
const remove_reject_button = document.getElementById('remove_reject_button');
const remove_friend_response = document.getElementById('remove_friend_response');

/**
 * This function opens/resets the modal for removing a friend 
 * from the users friends list.
 * @param {String} username the username of the friend that may be removed
 */
function openRemoveFriendModal(username){
    // Make accept/reject buttons visible
    remove_friend_button.style.display = "inline-block";
    remove_reject_button.style.display =  "inline-block";
    // Update text with friend's username
    remove_friend_name.innerHTML = "Would you like to remove " + username + " from your friends list?";
    // Make modal visible, blur background
    overlay.classList.remove("hidden");
    remove_friend_modal.style.display = "block";
    // Add proper functionality to button
    remove_friend_button.onclick = function() {
        removeFriend(username);
    };
}
/**
 * This function closes the modal for removing a friend from the users friends list.
 */
function closeRemoveFriendModal(){    // Make modal invisible
    overlay.classList.add("hidden");
    remove_friend_modal.style.display = "none";
}
/**
 * This function sends a POST request to remove a friend from the users friends list.
 * @param {String} friend_username 
 */
async function removeFriend(friend_username){
    // Make a POST request to remove friend from friends list
    const csrfToken = await getCSRFToken();
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
            // Hide buttons
            remove_friend_button.style.display = "none";
            remove_reject_button.style.display = "none";
            remove_friend_response.style.color = "green";
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


/**
 * 
 * Send friend request functionality
 * 
 */

// elements
const add_friend_modal = document.getElementById("add_friend_modal");
const add_friend_response = document.getElementById("add_friend_response");
const send_friend_username = document.getElementById("send_friend_username");

/**
 * This function opens/resets the modal for sending a friend request
 * to another user and blurs the background.
 */
function openAddFriendModal(){
    // Make response/username input empty
    add_friend_response.innerHTML = "";
    send_friend_username.value = "";
    // Make modal visible, blur background
    add_friend_modal.style.display = "block";
    overlay.classList.remove("hidden");
}
/**
 * This function closes the modal for sending a friend request.
 */
function closeAddFriendModal(){
    overlay.classList.add("hidden");
    add_friend_modal.style.display = "none";
}
/**
 * This function sends a POST request to send a friend request to another user.
 * @param {String} username the username of the user to send a friend request to
 */
async function sendFriendRequest(username){
    // Make a POST request to send friend request
    const csrfToken = await getCSRFToken();
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

/**
 * 
 * Received friend request functionality
 * 
 */

// elements
const friend_request_modal = document.getElementById("friend_request_modal");
const friend_request_response = document.getElementById("friend_request_response");
const friend_request_text = document.getElementById("friend_request_text");
const accept_friend_button = document.getElementById("accept_friend_button");
const reject_friend_button = document.getElementById("reject_friend_button");

/**
 * This function opens/resets the modal for accepting or rejecting a friend request
 * that the user has received.
 * @param {String} username the username of the user that sent the friend request
 */
function openFriendRequestModal(username){
    // Make response empty, update text with username
    friend_request_response.innerHTML = "";
    friend_request_text.innerHTML = username + " has sent you a friend request! Would you like to accept?";
    // Add functionality to buttons
    accept_friend_button.onclick = function() {
        confirmFriend(username);
    };
    reject_friend_button.onclick = function() {
        rejectFriend(username);
    };
    //Make modal/buttons visible and blur background
    friend_request_modal.style.display = "block";
    accept_friend_button.style.display = "inline-block";
    reject_friend_button.style.display = "inline-block";
    overlay.classList.remove("hidden");
    
}

/**
 * This function closes the modal for accepting or rejecting a friend request.
 */
function closeFriendRequestModal(){
    overlay.classList.add("hidden");
    friend_request_modal.style.display = "none";
}

/**
 * This function sends a POST request to accept a received friend request.
 * @param {String} friend_username the username of the user that sent the friend request
 */
async function confirmFriend(friend_username){
    // Make a POST request to add friend to friends list
    const csrfToken = await getCSRFToken();
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
            // Hide buttons
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

/**
 * This function sends a POST request to reject a received friend request.
 * @param {String} friend_username the username of the user that sent the friend request
 */
async function rejectFriend(friend_username){
    // Make a POST request to reject friend request
    const csrfToken = await getCSRFToken();
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
            // Hide buttons
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

/**
 * 
 * Send friend request functionality
 * 
 */

// elements
const delete_friend_modal = document.getElementById("delete_friend_request_modal");
const delete_friend_request_response = document.getElementById("delete_friend_request_response");
const delete_friend_request_text = document.getElementById("delete_friend_request_text");
const delete_friend_button = document.getElementById("yes_delete_friend_request_button");
const delete_reject_button = document.getElementById("no_delete_friend_request_button");

/**
 * This function opens/resets the modal for deleting a friend request the user has sent.
 * @param {String} username the username of the user that the friend request was sent to
 */
function openDeleteFriendRequestModal(username){
    // Reset response text, update text with username
    delete_friend_request_response.innerHTML = "";
    delete_friend_request_text.innerHTML = "Would you like to delete your friend request to " + username + "?";
    // Add functionality to buttons
    delete_friend_button.onclick = function() {
        deleteFriendRequest(username);
    };
    // Make modal/buttons visible and blur background
    delete_friend_modal.style.display = "block";
    overlay.classList.remove("hidden");
    delete_friend_button.style.display = "inline-block";
    delete_reject_button.style.display = "inline-block";
}
/**
 * This function closes the modal for deleting a friend request.
 */
function closeDeleteFriendRequestModal(){
    overlay.classList.add("hidden");
    delete_friend_modal.style.display = "none";
}

/**
 * This function sends a POST request to delete a friend request that the user has sent.
 * @param {String} friend_username the username of the user that the friend request was sent to
 */
async function deleteFriendRequest(friend_username){
    // Make a POST request to delete friend request
    const csrfToken = await getCSRFToken();
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
            // Hide buttons
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

