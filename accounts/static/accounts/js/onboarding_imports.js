const upload_modal = document.getElementById("upload_modal");
const upload_btn = document.getElementById("upload_btn");
const header = document.getElementById("top_header");

function openImdbModal() {
  upload_modal.classList.remove("hidden");
  overlay.classList.remove("hidden");
  header.innerHTML = "Upload your ratings file from IMDB";
  upload_btn.onclick = function () {
    uploadFile("imdb");
  };
}

function openBoxdModal() {
  upload_modal.classList.remove("hidden");
  overlay.classList.remove("hidden");
  header.innerHTML = "Upload your ratings file from Letterboxd";
  upload_btn.onclick = function () {
    uploadFile("letterboxd");
  };
}

function closeModal() {
  overlay.classList.add("hidden");
  upload_modal.classList.add("hidden");
  title.innerHTML = "Select File here";
  title.style.color = "black";
  subtitle.innerHTML = "Files Supported: CSV";
  document.getElementById("file").value = "";
}

overlay.addEventListener("click", closeModal);

const title = document.getElementById("title");
const subtitle = document.getElementById("subtitle");

async function uploadFile(source) {
  const csrfToken = await getCSRFToken();
  const file = document.getElementById("file").files[0];
  const formData = new FormData();
  formData.append("document", file);

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
