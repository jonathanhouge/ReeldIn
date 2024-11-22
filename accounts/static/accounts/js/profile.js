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

// For testing purposes
function clearLists() {
  fetch("/accounts/clear/lists/")
    .then((response) => {
      if (response.status === 200) {
        window.location.reload();
      }
    })
    .catch((error) => {
      console.error("Error clearing lists:", error);
    });
}

// Goes to movie page when user clicks movie poster
function goToMoviePage(movieId) {
  window.location.href = "/movie/" + movieId;
}

// Overlay element for background blur
const overlay = document.querySelector(".overlay");
var current_modal = null;

/****************************************************
 *
 * Remove friend functionality
 *
 ***************************************************/

const remove_friend_modal = document.getElementById("remove-friend-modal");
const remove_friend_name = document.getElementById("remove-friend-name");
const remove_friend_button = document.getElementById("remove-confirm-button");
const remove_reject_button = document.getElementById("remove-reject-button");
const remove_friend_response = document.getElementById(
  "remove-friend-response"
);

function closeCurrentModal() {
  current_modal.classList.add("hidden");
  overlay.classList.add("hidden");
}

/**
 * This function opens/resets the modal for removing a friend
 * from the users friends list.
 * @param {String} username the username of the friend that may be removed
 */
function openRemoveFriendModal(username) {
  remove_friend_button.classList.remove("hidden");
  remove_reject_button.classList.remove("hidden");

  remove_friend_response.innerHTML = "";
  remove_friend_name.innerHTML =
    "Would you like to remove " + username + " from your friends list?";

  overlay.classList.remove("hidden");
  remove_friend_modal.classList.remove("hidden");

  remove_friend_button.onclick = function () {
    removeFriend(username);
  };
  current_modal = remove_friend_modal;
}

/**
 * This function closes the modal for removing a friend from the users friends list.
 */
function closeRemoveFriendModal() {
  // Make modal invisible
  overlay.classList.add("hidden");
  remove_friend_modal.classList.add("hidden");
}

/**
 * This function sends a POST request to remove a friend from the users friends list.
 * @param {String} friend_username the username of the friend to be removed
 */
async function removeFriend(friend_username) {
  const csrfToken = await getCSRFToken();

  fetch("/accounts/remove/friend/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify({ username: friend_username }),
  })
    .then((response) => {
      if (response.status == 200) {
        remove_friend_button.classList.add("hidden");
        remove_reject_button.classList.add("hidden");
        remove_friend_response.style.color = "green";
        remove_friend_name.innerHTML = "";
        user_div = document.getElementById(friend_username + "-profile-div");
        user_div.remove();
      } else {
        remove_friend_response.style.color = "red";
      }
      checkDivEmpty("friends-list");
      return response.text();
    })
    .then((data) => {
      remove_friend_response.innerHTML = data;
    })
    .catch((error) => {
      console.log(
        "An error occured during the remove friend request: " + error
      );
    });
}

/****************************************************
 *
 * Send friend request functionality
 *
 ***************************************************/

const add_friend_modal = document.getElementById("add-friend-modal");
const add_friend_response = document.getElementById("add-friend-response");
const send_friend_username = document.getElementById("send-friend-username");

/**
 * This function opens/resets the modal for sending a friend request
 * to another user and blurs the background.
 */
function openAddFriendModal() {
  add_friend_response.innerHTML = "";
  send_friend_username.value = "";

  add_friend_modal.classList.remove("hidden");
  overlay.classList.remove("hidden");
  current_modal = add_friend_modal;
}

/**
 * This function closes the modal for sending a friend request.
 */
function closeAddFriendModal() {
  overlay.classList.add("hidden");
  add_friend_modal.classList.add("hidden");
}

/**
 * This function sends a POST request to send a friend request to another user.
 * @param {String} username the username of the user to send a friend request to
 */
async function sendFriendRequest(username) {
  const csrfToken = await getCSRFToken();
  const name_input = send_friend_username.value;

  fetch("/accounts/send/friend/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify({ username: name_input }),
  })
    .then((response) => {
      if (response.status == 200) {
        add_friend_response.style.color = "green";
        send_friend_username.value = "";
      } else {
        add_friend_response.style.color = "red";
      }
      return response.json();
    })
    .then((data) => {
      add_friend_response.innerHTML = data.message;
      if (data.receiver) {
        addUserToSentRequests(data.receiver);
        checkDivEmpty("sent-requests");
      }
    })
    .catch((error) => {
      console.log("An error occured during the add friend request: " + error);
    });
}

function addUserToSentRequests(user) {
  const sent_requests = document.getElementById("sent-requests");
  const user_div = document.createElement("div");
  user_div.id = user.username + "-profile-div";
  user_div.classList.add("friend");
  user_div.setAttribute(
    "onclick",
    `openDeleteFriendRequestModal('${user.username}')`
  );
  user_div.innerHTML = `
    <img
    src='${user.profile_picture}'
    class="profile-img" 
    />
    <h3>${user.username}</h3>
  `;
  sent_requests.appendChild(user_div);
}

/****************************************************
 *
 * Received friend request functionality
 *
 ***************************************************/

const friend_request_modal = document.getElementById("friend-request-modal");
const friend_request_response = document.getElementById(
  "friend-request-response"
);
const friend_request_text = document.getElementById("friend-request-text");
const acceptFriendButton = document.getElementById("accept-friend-button");
const rejectFriendButton = document.getElementById("reject-friend-button");

/**
 * This function opens/resets the modal for accepting or rejecting a friend request
 * that the user has received.
 * @param {String} username the username of the user that sent the friend request
 */
function openFriendRequestModal(username) {
  friend_request_response.innerHTML = "";
  friend_request_text.innerHTML =
    username + " has sent you a friend request! Would you like to accept?";

  acceptFriendButton.onclick = function () {
    confirmFriend(username);
  };
  rejectFriendButton.onclick = function () {
    rejectFriend(username);
  };

  friend_request_modal.classList.remove("hidden");
  acceptFriendButton.classList.remove("hidden");
  rejectFriendButton.classList.remove("hidden");
  overlay.classList.remove("hidden");
  current_modal = friend_request_modal;
}

/**
 * This function closes the modal for accepting or rejecting a friend request.
 */
function closeFriendRequestModal() {
  overlay.classList.add("hidden");
  friend_request_modal.classList.add("hidden");
}

/**
 * This function sends a POST request to accept a received friend request.
 * @param {String} friend_username the username of the user that sent the friend request
 */
async function confirmFriend(friend_username) {
  const csrfToken = await getCSRFToken();
  fetch("/accounts/accept/friend/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify({ username: friend_username }),
  })
    .then((response) => {
      if (response.status == 200) {
        acceptFriendButton.classList.add("hidden");
        rejectFriendButton.classList.add("hidden");
        friend_request_response.style.color = "green";
        friend_request_text.innerHTML = "";

        user_div = document.getElementById(friend_username + "-profile-div");
        console.log("Changing attribute to openRemoveFriendModal");
        user_div.setAttribute(
          "onclick",
          `openRemoveFriendModal('${friend_username}')`
        );
        user_div.remove();

        friendsList = document.getElementById("friends-list");
        friendsList.appendChild(user_div);
        checkDivEmpty("friends-list");
        checkDivEmpty("received-requests");
      } else {
        friend_request_response.style.color = "red";
      }

      return response.text();
    })
    .then((data) => {
      friend_request_response.innerHTML = data;
    })
    .catch((error) => {
      console.log(
        "An error occured during the accept friend request: " + error
      );
    });
}

function checkDivEmpty(div_name) {
  div = document.getElementById(div_name);
  console.log(div.childElementCount);
  if (div.childElementCount == 1) {
    div_text = document.getElementById(div_name + "-text");
    div_text.classList.remove("hidden");
  } else {
    div_text = document.getElementById(div_name + "-text");
    div_text.classList.add("hidden");
  }
}

/**
 * This function sends a POST request to reject a received friend request.
 * @param {String} friend_username the username of the user that sent the friend request
 */
async function rejectFriend(friend_username) {
  const csrfToken = await getCSRFToken();
  fetch("/accounts/delete/friend_request/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify({
      username: friend_username,
      username_is_sender: true,
    }),
  })
    .then((response) => {
      if (response.status == 200) {
        acceptFriendButton.classList.add("hidden");
        rejectFriendButton.classList.add("hidden");
        friend_request_response.style.color = "green";
        friend_request_text.innerHTML = "";
        user_div = document.getElementById(friend_username + "-profile-div");
        user_div.remove();
        checkDivEmpty("received-requests");
      } else {
        friend_request_response.style.color = "red";
      }

      return response.text();
    })
    .then((data) => {
      friend_request_response.innerHTML = data;
    })
    .catch((error) => {
      console.log(
        "An error occured during the reject friend request: " + error
      );
    });
}

/****************************************************
 *
 * Delete sent friend request functionality
 *
 ***************************************************/

// elements
const delete_friend_modal = document.getElementById(
  "delete-friend-request-modal"
);
const delete_friend_request_response = document.getElementById(
  "delete-friend-request-response"
);
const delete_friend_request_text = document.getElementById(
  "delete-friend-request-text"
);
const delete_friend_button = document.getElementById(
  "yes-delete-friend-request-button"
);
const delete_reject_button = document.getElementById(
  "no-delete-friend-request-button"
);

/**
 * This function opens/resets the modal for deleting a friend request the user has sent.
 * @param {String} username the username of the user that the friend request was sent to
 */
function openDeleteFriendRequestModal(username) {
  delete_friend_request_response.innerHTML = "";
  delete_friend_request_text.innerHTML =
    "Would you like to delete your friend request to " + username + "?";

  delete_friend_button.onclick = function () {
    deleteFriendRequest(username);
  };

  delete_friend_modal.classList.remove("hidden");
  overlay.classList.remove("hidden");
  delete_friend_button.classList.remove("hidden");
  delete_reject_button.classList.remove("hidden");
  current_modal = delete_friend_modal;
}

/**
 * This function closes the modal for deleting a friend request.
 */
function closeDeleteFriendRequestModal() {
  overlay.classList.add("hidden");
  delete_friend_modal.classList.add("hidden");
}

/**
 * This function sends a POST request to delete a friend request that the user has sent.
 * @param {String} friend_username the username of the user that the friend request was sent to
 */
async function deleteFriendRequest(friend_username) {
  const csrfToken = await getCSRFToken();
  fetch("/accounts/delete/friend_request/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify({
      username: friend_username,
      username_is_sender: false,
    }),
  })
    .then((response) => {
      if (response.status == 200) {
        delete_friend_button.classList.add("hidden");
        delete_reject_button.classList.add("hidden");
        delete_friend_request_response.style.color = "green";
        delete_friend_request_text.innerHTML = "";
        user_div = document.getElementById(friend_username + "-profile-div");
        user_div.remove();
        checkDivEmpty("sent-requests");
      } else {
        delete_friend_request_response.style.color = "red";
      }

      return response.text();
    })
    .then((data) => {
      delete_friend_request_response.innerHTML = data;
    })
    .catch((error) => {
      console.log(
        "An error occured during the delete friend request: " + error
      );
    });
}
