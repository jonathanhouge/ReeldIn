const delete_modal = document.getElementById("delete_account_modal");
const change_modal = document.getElementById("change_modal");
const profile_modal = document.getElementById("profile-pic-modal"); // TODO doesn't exist

const title = document.getElementById("title");
const subtitle = document.getElementById("subtitle");

const change_btn = document.getElementById("change_btn");
const input = document.querySelector(".current_input");
const deleteAccountBtn = document.querySelector(".delete-account-btn");

const overlay = document.getElementById("overlay");

function openDeleteModal() {
  delete_modal.classList.remove("hidden");
  overlay.classList.remove("hidden");
}

function closeDeleteModal() {
  overlay.classList.add("hidden");
  delete_modal.classList.add("hidden");
}

function openProfilePicModal() {
  upload_modal.classList.remove("hidden");
  overlay.classList.remove("hidden");
}

function closeProfilePicModal() {
  overlay.classList.add("hidden");
  upload_modal.classList.add("hidden");
}

function openChangeUsernameModal() {
  change_modal.classList.remove("hidden");
  overlay.classList.remove("hidden");
  title.innerHTML = "Change Username";
  subtitle.innerHTML = "Enter your new username";
  change_btn.addEventListener("click", function () {
    change("username");
  });
  input.setAttribute("placeholder", "New Username");
  input.setAttribute("id", "username");
}

function openChangePasswordModal() {
  change_modal.classList.remove("hidden");
  overlay.classList.remove("hidden");
  title.innerHTML = "Change Password";
  subtitle.innerHTML = "Enter your new password";
  change_btn.addEventListener("click", function () {
    change("password");
  });
  input.setAttribute("placeholder", "New Password");
  input.setAttribute("id", "password");
}

function closeChangeModal() {
  overlay.classList.add("hidden");
  change_modal.classList.add("hidden");
  title.innerHTML = "";
  subtitle.innerHTML = "";
}

overlay.addEventListener("click", closeModal);

async function change(value) {
  const csrfToken = await getCSRFToken();

  if (value === "username") {
    const username = document.getElementById("username").value;
    console.log(username);
  } else {
    const password = document.getElementById("password").value;
    console.log(password);
  }

  change_btn.innerHTML = "Changing " + value + "...";
  fetch("/accounts/change/" + value + "/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify({ username: username, password: password }),
  })
    .then((response) => {
      if (response.status === 200) {
        console.log("Success");
        title.innerHTML =
          value.charAt(0).toUpperCase() +
          value.slice(1) +
          "changed successfully!";
        title.style.color = "green";
      } else {
        title.innerHTML = "Error!";
        title.style.color = "red";
        console.log("Error");
      }
      return response.text();
    })
    .then((text) => {
      subtitle.innerHTML = text;
      console.log("Text" + text);
    });
}

async function uploadFile(source) {
  const csrfToken = await getCSRFToken();
  const file = document.getElementById("file").files[0];
  const formData = new FormData();
  formData.append("document", file);
  upload_btn.innerHTML = "Uploading Picture...";

  fetch("/accounts/onboarding/upload/", {
    method: "POST",
    enctype: "multipart/form-data",
    headers: {
      "X-CSRFToken": csrfToken,
    },
    body: formData,
  })
    .then((response) => {
      if (response.status === 200) {
        console.log("Success");
        title.innerHTML = "File uploaded successfully!";
        title.style.color = "green";
        upload_btn.innerHTML = "Upload";
      } else {
        title.innerHTML = "Error!";
        title.style.color = "red";
        console.log("Error");
        upload_btn.innerHTML = "Upload";
      }
      return response.text();
    })
    .then((text) => {
      subtitle.innerHTML = text;
      console.log("Text" + text);
    });
}

async function deleteAccount() {
  const csrfToken = await getCSRFToken();
  fetch("/accounts/delete/account", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
  })
    .then((response) => {
      if (response.status === 200) {
        console.log("Success");
        title.innerHTML = "Account Deleted!";
        title.style.color = "green";
        deleteAccountBtn.innerHTML = "Return";
        deleteAccountBtn.onclick = function () {
          window.location.href = "/";
        };
        overlay.onclick = function () {
          window.location.href = "/";
        };
      } else {
        title.innerHTML = "Error!";
        title.style.color = "red";
        console.log("Error");
      }
      return response.text();
    })
    .then((text) => {
      subtitle.innerHTML = text;
      console.log("Text" + text);
    });
}

function closeModal() {
  closeDeleteModal();
  closeChangeModal();
  closeProfilePicModal();
}
