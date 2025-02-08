document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector("form");

  form.addEventListener("submit", function (event) {
    const inputs = document.querySelectorAll("input, select");
    let valid = true;

    inputs.forEach((input) => {
      if (!input.value) {
        input.style.border = "2px solid red";
        valid = false;
      } else {
        input.style.border = "1px solid #ccc";
      }
    });

    if (!valid) {
      event.preventDefault();
      alert("Please fill in all fields before submitting.");
    }
  });
});
