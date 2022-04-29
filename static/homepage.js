// Constant link to the welcome message
const welcomeMsg = document.getElementById("welcomeMsg");
// Constant link to the Log out button
// const myButtonOut = document.getElementById("myButtonOut");
// Constant with the "username" part of the keyItem (to be used with localstorage)
// const keyItem = "username";
// Constant link to the Delete your account link
const deleteLink = document.getElementById("deleteLink");
// Variable storing the active user
let activeUser = "o";

// Function to modify the welcome message
function changeWelcome(){
  // Get the active username
  activeUser = localStorage.getItem("activeSelector");
  if (localStorage.getItem(activeUser) != -1){
    // Add the username to the welcome message
    welcomeMsg.innerText = "Welcome " + activeUser;
  }
}

// Delete the content of localstorage for the active user and reload the page
function deleteAccount(){
  localStorage.removeItem(activeUser);
  location.reload();
}

// Call the function to add the username to the welcome message
changeWelcome();

// Call deleteAccount function when clicked on Delete your account link
deleteLink.addEventListener("click", deleteAccount);
