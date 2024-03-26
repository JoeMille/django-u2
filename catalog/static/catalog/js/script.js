
// Header image pulsating effect

// Header image pulsating effect
const header = document.querySelector('.site-header');
const featuredProducts = document.querySelector('.featured-products');
let brightness = 1;

setInterval(() => {
    brightness = brightness === 1 ? 1.5 : 1;
    if (header) {
        header.style.filter = `brightness(${brightness})`;
    }
    if (featuredProducts) {
        featuredProducts.style.filter = `brightness(${brightness})`;
    }
}, 2000);

// code for particles.js background
window.addEventListener('load', function() {
    if (typeof particlesJS !== 'undefined') {
        particlesJS.load('particles-js', particlesJsonUrl, function() {
            console.log('particles.js loaded - callback');
        });
    }
});

// Product image carousel
function rotate() {
    var lastChild = $('.slider div:last-child').clone();
    /*$('#test').html(lastChild)*/
    $('.slider div').removeClass('firstSlide')
    $('.slider div:last-child').remove();
    $('.slider').prepend(lastChild)
    $(lastChild).addClass('firstSlide')
  }
  
  window.setInterval(function(){
    rotate()
  }, 4000);
  

// Stripe Js payment form 
// To use this payment method live, you must switch to HTTPs to ensure secure data transfer

var stripe = Stripe('pk_test_51Own3jFlpTEzDIrEWgl8A3ChU9v5tddxPbVh8VTxHJJHAXU0nzAVBRGGvap56gncNJuVudSf0uixGMrU77It6sUV00qCFkadDE');
var elements = stripe.elements();

var card = elements.create('card');

// Check if #card-element exists before mounting
if (document.querySelector('#card-element')) {
    card.mount('#card-element');
}

var form = document.getElementById('payment-form');
if (form) {
    form.addEventListener('submit', function(event) {
        event.preventDefault();

        stripe.createToken(card).then(function(result) {
            if (result.error) {
                var errorElement = document.getElementById('card-errors');
                errorElement.textContent = result.error.message;
            } else {
                stripeTokenHandler(result.token);
            }
        });
    });
}

// Submit Stripe form to Django

function stripeTokenHandler(token) {
    var form = document.getElementById('payment-form');
    if (form) {
        var hiddenInput = document.createElement('input');
        hiddenInput.setAttribute('type', 'hidden');
        hiddenInput.setAttribute('name', 'stripeToken');
        hiddenInput.setAttribute('value', token.id);
        form.appendChild(hiddenInput);

        form.submit();
    }
}

// Validate review rating field max value 10 REVIEWS PAGE FORM

window.onload = function() {
    var reviewForm = document.getElementById('reviewForm');
    if (reviewForm) {
        reviewForm.addEventListener('submit', function(event) {
            var rating = document.getElementById('rating').value;
            if (rating < 1 || rating > 10) {
                alert('Rating must be between 1 and 10.');
                event.preventDefault();
            }
        });
    }
}




console.log("JavaScript is being loaded!");