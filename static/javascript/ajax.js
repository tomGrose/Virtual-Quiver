
document.addEventListener("DOMContentLoaded", function(event) {
    const discsContainer = document.querySelector("#discs-display-container");

    discsContainer.addEventListener("click", function(evt){
        if (evt.target.tagName === 'BUTTON'){
            const discId = evt.target.getAttribute('data-id');
            const button = evt.target;
            if (button.getAttribute('data-button-type') === "add-to-bag"){
                handleDiscAdd(discId);
            }
            else if (button.getAttribute('data-button-type') === "add-to-wishlist"){
                handleWishlistAdd(discId)
            }
            buttonChange(evt.target);
        }
        
    })
  });

async function handleDiscAdd(discId){
    resp = await axios.post('http://127.0.0.1:5000/discs/add', {'disc_id': discId});
}

async function handleWishlistAdd(discId){
    resp = await axios.post('http://127.0.0.1:5000/discs/wishlist/add', {'disc_id': discId});
}