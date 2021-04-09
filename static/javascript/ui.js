// Change the button's text when a user already has this disc in their bag or their wishlist
function buttonChange(button) {
    if (button.getAttribute('data-button-type') === "add-to-bag"){
        const buttonId = button.getAttribute('data-id')
        const wishButton = document.querySelector(`#wish-${buttonId}`)
        button.innerHTML = "Added to quiver";
        wishButton.remove();
    }
    else if (button.getAttribute('data-button-type') === "add-to-wishlist"){
        button.innerHTML = "Added to wishlist";
    }
}


// Create an event listener to populate the range values from the discover discs search page when it is loaded
// also listen for the buttons to be pressed on the account page to dynamically display the account delete form
document.addEventListener("DOMContentLoaded", function(event) {
    try{
        handleSearchValues();
    } catch(ex) {}
    
    try{
        document.querySelector('#user-profile-card').addEventListener("click", (evt) => {
        
            if (evt.target.getAttribute('id') === "account-delete-btn"){
                handleDeleteForm();
            }
            if (evt.target.getAttribute('id') === "cancel-delete-btn"){
                evt.preventDefault();
                handleDeleteCancel();
            }
        }) 
    } catch(ex) {}

    try{
        document.querySelector('#home-view-select').addEventListener("change", (evt) => {
            handleHomeView();
        }) 
    } catch(ex) {}
  });


// Populate the range sliders on the discover page with their corresponding values
function handleSearchValues(){
    const outputs = [document.querySelector('#difficultyIdVal'),
        document.querySelector('#speedIdVal'),
        document.querySelector('#glideIdVal'),
        document.querySelector('#low_stabilityIdVal'),
        document.querySelector('#high_stabilityIdVal')];

    const inputs = [document.querySelector('#difficultyId'),
        document.querySelector('#speedId'),
        document.querySelector('#glideId'),
        document.querySelector('#high_stabilityId'),
        document.querySelector('#low_stabilityId')];


    outputs.forEach((val, indx) => {
        val.value = inputs[indx].value
    })
}


// Show the delete form to a user when they click delete account
function handleDeleteForm(){
    document.querySelector('#account-delete-btn').hidden = true;
    const deleteForm = document.querySelector('#account-delete-form');
    deleteForm.hidden = false;
}

// Hide the delete account form when a user clicks cancel
function handleDeleteCancel() {
    document.querySelector('#account-delete-btn').hidden = false;
    const deleteForm = document.querySelector('#account-delete-form');
    deleteForm.hidden = true;
}

// Remove a disc card from a users wishlist when the have added it to their bag
function removeDiscCard(button) {
    const discId = button.getAttribute('data-id');
    const discCard = document.getElementById(`${discId}-card`);
    discCard.remove();
}

// Dynamically change the homepage based off of the user's input

function handleHomeView() {
    console.log('HIHIHIHIHIHIHIHIH')
    selectVal = document.querySelector('#home-view-select').value;

    if (selectVal === "quiver"){
        document.querySelector('#discs-display-container').hidden = false;
        document.querySelector('#users-wishlist-container').hidden = true;
    } else if (selectVal === 'wishlist'){
        document.querySelector('#users-wishlist-container').hidden = false;
        document.querySelector('#discs-display-container').hidden = true;
    }
}