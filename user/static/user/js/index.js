document.addEventListener("DOMContentLoaded", function () {
  const password = document.getElementById("id_password");
  const confirmPassword = document.getElementById("id_confirm_password");
  const errorMessage = document.createElement("p");
  const submit_btn = document.getElementById("submit_form");

  errorMessage.style.color = "red";
  errorMessage.style.fontSize = "14px";
  errorMessage.style.marginTop = "5px";
  confirmPassword.parentNode.appendChild(errorMessage);

  function validatePassword() {
    if (password.value !== confirmPassword.value) {
      errorMessage.textContent = "Passwords do not match";
      submit_btn.disabled = true;
      submit_btn.classList.add("cursor-not-allowed");
    } else {
      errorMessage.textContent = "";
      submit_btn.disabled = false;
      submit_btn.classList.remove("cursor-not-allowed");
    }
  }

  password.addEventListener("input", validatePassword);
  confirmPassword.addEventListener("input", validatePassword);
});
