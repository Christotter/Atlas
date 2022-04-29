// Constant link to the login submit button
const myButton = document.getElementById("myButton");
// Constant link to the Username field
const myUsername = document.getElementById("myUsername");
// Constant with the "username" part of the keyItem (to be used with localstorage)
const keyItem = "username";
// Variable storing the active user
let activeUser = "o";

// Function to get the username entered by the user, store it
// in the LocalStorage and call a function to modify the welcome message
function getUsername(){
  var nameRegex = /^[a-zA-Z]+$/;
  var validUsername = myUsername.value.match(nameRegex);
  if(validUsername == null){
      alert("Your first name is not valid. Only characters A-Z, a-z are acceptable.");
      myUsername.focus();
      return false;
  } else {
    // Storing the active user in local storage as "username" + actual username
    // Paired with the key "activeSelector"
    activeUser = keyItem + myUsername.value;
    localStorage.setItem("activeSelector", myUsername.value);
    const test = localStorage.getItem(activeUser);

    // Test if the user doesn't exist and store it in localstorage
    if(test == false){
      localStorage.setItem(keyItem + myUsername.value, myUsername.value);
      activeUser = keyItem + myUsername.value;
    }
  }
}

// Clear the username field from it's description when the user click on it
function clearField(){
  myUsername.value = "";
}

// Call getUsername function when clicked on submit button
myButton.addEventListener("click", getUsername);
// Call clearField function when clicked on the username field
myUsername.addEventListener("click", clearField);
