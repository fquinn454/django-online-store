const address = window.location.pathname.substring(1);
const navLinks = document.getElementsByClassName('nav-link')
let favouriteCount = 0;
let cartCount = 0;

window.addEventListener("load", () => {
    for (i = 0; i < navLinks.length; i++){
        if (navLinks[i].id === address){
            navLinks[i].className += ' disabled';
        }
    }
});

function addFavourite(){
    let favouriteCounter = document.getElementById('favourite-counter');
    favouriteCount += 1;
    favouriteCounter.innerHTML = favouriteCount;
}

function addToCart(){
    let cartCounter = document.getElementById('cart-counter');
    cartCount += 1;
    cartCounter.innerHTML = cartCount;
}