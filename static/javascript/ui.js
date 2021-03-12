function buttonChange(button) {
    if (button.getAttribute('data-button-type') === "add-to-bag"){
        button.innerHTML = "Added to quiver";
    }
    else if (button.getAttribute('data-button-type') === "add-to-wishlist"){
        button.innerHTML = "Added to wishlist";
    }
}