
document.addEventListener("DOMContentLoaded", function(event) {
    const discsContainer = document.querySelector("#discs-display-container");
    const wishContainer = document.querySelector('#users-wishlist-container');

    try{
        discsContainer.addEventListener("click", function(evt){
            if (evt.target.tagName === 'BUTTON'){
                const discId = evt.target.getAttribute('data-id');
                const button = evt.target;
                if (button.getAttribute('data-button-type') === "add-to-bag"){
                    handleDiscAdd(discId);
                    buttonChange(evt.target);
                } else if (button.getAttribute('data-button-type') === "add-to-wishlist"){
                    handleWishlistAdd(discId);
                    buttonChange(evt.target);
                } else if (button.getAttribute('data-button-type') === "remove-from-bag") {
                    removeDiscCard(button);
                    handleRemoveFromBag(discId);
                }
            } 
        })
    } catch(ex) {}

    try {
        wishContainer.addEventListener('click', (evt) => {
            if (evt.target.getAttribute('data-button-type') === "wishlist-add-to-bag"){
                const discId = evt.target.getAttribute('data-id');
                removeDiscCard(evt.target);
                handleRemoveFromWishlist(discId);
                handleDiscAdd(discId);
            }
        })
        wishContainer.addEventListener('click', (evt) => {
            if (evt.target.getAttribute('data-button-type') === "wishlist-remove"){
                const discId = evt.target.getAttribute('data-id');
                removeDiscCard(evt.target);
                handleRemoveFromWishlist(discId);
            }
        })
    } catch(ex){}
    
});

async function handleDiscAdd(discId){
    resp = await axios.post('http://127.0.0.1:5000/discs/add', {'disc_id': discId});
}

async function handleWishlistAdd(discId){
    resp = await axios.post('http://127.0.0.1:5000/discs/wishlist/add', {'disc_id': discId});
}

async function handleRemoveFromWishlist(discId){
    resp = await axios.post('http://127.0.0.1:5000/discs/wishlist/remove', {'disc_id': discId});
}

async function handleRemoveFromBag(discId){
    resp = await axios.post('http://127.0.0.1:5000/discs/remove', {'disc_id': discId});
}