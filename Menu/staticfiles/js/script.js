/* 
Table of Contents:
1. Tab Management System
2. Phone Number Validation
   - Initialization
   - Error Handling
   - Event Listeners
*/

/* ----------------------------------------Tab Management System starts ---------------------------------------- */
let tabcontents = document.getElementsByClassName('tab-content');

function opentab(arg) {
    for (let tabcontent of tabcontents) {
        tabcontent.classList.remove('active-tab'); // Remove active class from all tabs
    }
    document.getElementById(arg).classList.add('active-tab'); // Add active class to the clicked tab
}
/* ----------------------------------------Tab Management System ends ---------------------------------------- */

/* ----------------------------------------Phone Number Validation starts ---------------------------------------- */
/* ----------------------------------------Initialization starts ---------------------------------------- */
const input = document.querySelector("#phone");
const button = document.querySelector("#btn");
const errorMsg = document.querySelector("#error-msg");
const validMsg = document.querySelector("#valid-msg");

// Only initialize if the phone input element exists
if (input) {
    // Error messages for different validation scenarios
    const errorMap = ["Invalid number", "Invalid country code", "Too short", "Too long", "Invalid number"];

    // Initialize international telephone input plugin
    const iti = window.intlTelInput(input, {
      initialCountry: "us",
      loadUtils: () => import("/intl-tel-input/js/utils.js?1733756310855"),
    });
    /* ----------------------------------------Initialization ends ---------------------------------------- */

    /* ----------------------------------------Error Handling starts ---------------------------------------- */
    // Reset validation state and messages
    const reset = () => {
      input.classList.remove("error");
      errorMsg.innerHTML = "";
      errorMsg.classList.add("hide");
      validMsg.classList.add("hide");
    };

    // Display error message
    const showError = (msg) => {
      input.classList.add("error");
      errorMsg.innerHTML = msg;
      errorMsg.classList.remove("hide");
    };
    /* ----------------------------------------Error Handling ends ---------------------------------------- */

    /* ----------------------------------------Event Listeners starts ---------------------------------------- */
    // Validate phone number on button click
    if (button) {
        button.addEventListener('click', () => {
          reset();
          if (!input.value.trim()) {
            showError("Required");
          } else if (iti.isValidNumber()) {
            validMsg.classList.remove("hide");
          } else {
            const errorCode = iti.getValidationError();
            const msg = errorMap[errorCode] || "Invalid number";
            showError(msg);
          }
        });
    }

    // Reset validation on input change
    input.addEventListener('change', reset);
    input.addEventListener('keyup', reset);
    /* ----------------------------------------Event Listeners ends ---------------------------------------- */
}
/* ----------------------------------------Phone Number Validation ends ---------------------------------------- */

/* ----------------------------------------Show Password Functionality starts ---------------------------------------- */
const showPasswordCheckbox = document.getElementById('show_password');

if (showPasswordCheckbox) {
    showPasswordCheckbox.addEventListener('change', function() {
        const passwordFields = document.querySelectorAll('input[type="password"]');
        passwordFields.forEach(function(field) {
            field.type = showPasswordCheckbox.checked ? 'text' : 'password';
        });
    });
}
/* ----------------------------------------Show Password Functionality ends ---------------------------------------- */
